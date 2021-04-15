import unittest

from django.core.management import call_command
from parameterized import parameterized

from hct_mis_api.apps.targeting.models import (
    HouseholdSelection,
    TargetingCriteria,
    TargetingCriteriaRule,
    TargetingCriteriaRuleFilter,
    TargetPopulation,
)
from hct_mis_api.apps.account.fixtures import UserFactory
from hct_mis_api.apps.account.permissions import Permissions
from hct_mis_api.apps.core.base_test_case import APITestCase
from hct_mis_api.apps.core.models import BusinessArea
from hct_mis_api.apps.household.fixtures import create_household


@unittest.skip("fix ordering")
class TestTargetPopulationQuery(APITestCase):
    ALL_TARGET_POPULATION_QUERY = """
            query AllTargetPopulation($finalListTotalHouseholdsMin: Int) {
                allTargetPopulation(finalListTotalHouseholdsMin:$finalListTotalHouseholdsMin, businessArea: "afghanistan") {
                    edges {
                        node {
                             name
                             status
                            candidateListTotalHouseholds
                            candidateListTotalIndividuals
                            finalListTotalHouseholds
                            finalListTotalIndividuals
                        }
                    }
                }
            }
            """
    TARGET_POPULATION_QUERY = """
       query TargetPopulation($id:ID!) {
          targetPopulation(id:$id){
            name
            status
            candidateListTotalHouseholds
            candidateListTotalIndividuals
            finalListTotalHouseholds
            finalListTotalIndividuals
            candidateListTargetingCriteria{
              rules{
                filters{
                  comparisionMethod
                  fieldName
                  isFlexField
                  arguments
                  fieldAttribute{
                    labelEn
                    type
                  }
                }
              }
            }
            finalListTargetingCriteria{
              rules{
                filters{
                  comparisionMethod
                  fieldName
                  isFlexField
                  arguments
                }
              }
            }
          }
        }
                """

    @classmethod
    def setUpTestData(cls):
        call_command("loadbusinessareas")
        cls.business_area = BusinessArea.objects.get(slug="afghanistan")
        _ = create_household(
            {"size": 1, "residence_status": "HOST", "business_area": cls.business_area},
        )
        (household, individuals) = create_household(
            {"size": 1, "residence_status": "HOST", "business_area": cls.business_area},
        )
        cls.household_size_1 = household
        cls.household_residence_status_citizen = cls.household_size_1
        (household, individuals) = create_household(
            {"size": 2, "residence_status": "REFUGEE", "business_area": cls.business_area},
        )
        cls.household_residence_status_refugee = household
        cls.household_size_2 = cls.household_residence_status_refugee

        cls.user = UserFactory.create()
        targeting_criteria = cls.get_targeting_criteria_for_rule(
            {"field_name": "size", "arguments": [2], "comparision_method": "EQUALS"}
        )
        cls.target_population_size_2 = TargetPopulation(
            name="target_population_size_2",
            created_by=cls.user,
            candidate_list_targeting_criteria=targeting_criteria,
            business_area=cls.business_area,
        )
        cls.target_population_size_2.save()
        targeting_criteria = cls.get_targeting_criteria_for_rule(
            {"field_name": "residence_status", "arguments": ["REFUGEE"], "comparision_method": "EQUALS"}
        )
        cls.target_population_residence_status = TargetPopulation(
            name="target_population_residence_status",
            created_by=cls.user,
            business_area=cls.business_area,
            candidate_list_targeting_criteria=targeting_criteria,
        )
        cls.target_population_residence_status.save()

        targeting_criteria = cls.get_targeting_criteria_for_rule(
            {"field_name": "size", "arguments": [1], "comparision_method": "EQUALS"}
        )
        cls.target_population_size_1_approved = TargetPopulation(
            name="target_population_size_1_approved",
            created_by=cls.user,
            candidate_list_targeting_criteria=targeting_criteria,
            status=TargetPopulation.STATUS_APPROVED,
            business_area=cls.business_area,
        )
        cls.target_population_size_1_approved.save()
        HouseholdSelection.objects.create(
            household=cls.household_size_1,
            target_population=cls.target_population_size_1_approved,
        )

    @staticmethod
    def get_targeting_criteria_for_rule(rule_filter):
        targeting_criteria = TargetingCriteria()
        targeting_criteria.save()
        rule = TargetingCriteriaRule(targeting_criteria=targeting_criteria)
        rule.save()
        rule_filter = TargetingCriteriaRuleFilter(**rule_filter, targeting_criteria_rule=rule)
        rule_filter.save()
        return targeting_criteria

    @unittest.skip("needs adjudication")
    @parameterized.expand(
        [
            (
                "with_permission",
                [Permissions.TARGETING_VIEW_LIST],
                {},
            ),
            ("without_permission", [], {}),
            (
                "with_permission_filter_finalListTotalHouseholdsMin",
                [Permissions.TARGETING_VIEW_LIST],
                {"finalListTotalHouseholdsMin": 1},
            ),
        ]
    )
    def test_simple_all_targets_query(self, _, permissions, variables):
        self.create_user_role_with_permissions(self.user, permissions, self.business_area)

        self.snapshot_graphql_request(
            request_string=TestTargetPopulationQuery.ALL_TARGET_POPULATION_QUERY,
            context={"user": self.user},
            variables=variables,
        )

    @parameterized.expand(
        [
            (
                "with_permission",
                [Permissions.TARGETING_VIEW_DETAILS],
            ),
            (
                "without_permission",
                [],
            ),
        ]
    )
    def test_simple_target_query(self, _, permissions):
        self.create_user_role_with_permissions(self.user, permissions, self.business_area)

        self.snapshot_graphql_request(
            request_string=TestTargetPopulationQuery.TARGET_POPULATION_QUERY,
            context={"user": self.user},
            variables={
                "id": self.id_to_base64(
                    self.target_population_size_1_approved.id,
                    "TargetPopulationNode",
                )
            },
        )

    @parameterized.expand(
        [
            (
                "with_permission",
                [Permissions.TARGETING_VIEW_DETAILS],
            ),
            (
                "without_permission",
                [],
            ),
        ]
    )
    def test_simple_target_query_2(self, _, permissions):
        self.create_user_role_with_permissions(self.user, permissions, self.business_area)

        self.snapshot_graphql_request(
            request_string=TestTargetPopulationQuery.TARGET_POPULATION_QUERY,
            context={"user": self.user},
            variables={
                "id": self.id_to_base64(
                    self.target_population_residence_status.id,
                    "TargetPopulationNode",
                )
            },
        )