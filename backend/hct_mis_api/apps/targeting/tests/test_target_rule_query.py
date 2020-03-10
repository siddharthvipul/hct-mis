import datetime as dt
import json

from account.fixtures import UserFactory
from core.base_test_case import APITestCase
from core.fixtures import LocationFactory
from household.fixtures import HouseholdFactory
from household.fixtures import IndividualFactory
from registration_data.fixtures import RegistrationDataImportFactory
from targeting.fixtures import TargetPopulationFactory
from targeting.fixtures import TargetRuleFactory


class TestTargetRuleQuery(APITestCase):
    """Computes Target Households Results based on TargetRules."""

    @classmethod
    def setUpTestData(cls):
        # graph query to be called.
        cls.FILTER_QUERY = """
        query TargetRules($serializedList: String!) {
            targetRules(serializedList: $serializedList) {
                householdCaId
                headOfHousehold {
                    fullName
                    firstName
                    lastName
                    dob
                }
                familySize
                address
                location {
                    title
                }
                registrationDataImportId {
                    name
                }
            }
        }
        """
        cls.user = UserFactory.create()
        intake_group = "some group name"
        argument_payload = [
            {
                "core_rules": {
                    "intake_group": intake_group,
                    "sex": "M",
                    # TODO(codecakes): enable when we can map school distance to right model.
                    # "school_distance_min": 1,
                    # "school_distance_min": 10,
                    "num_individuals_min": 2,
                    "num_individuals_max": 6,
                },
                "flex_rules": {"age_min": 1, "age_max": 39,},
            },
            {
                "core_rules": {
                    "intake_group": intake_group,
                    "sex": "F",
                    # "school_distance_min": 1,
                    # "school_distance_min": 10,
                    "num_individuals_min": 2,
                    "num_individuals_max": 6,
                },
                "flex_rules": {"age_min": 10, "age_max": 31,},
            },
        ]
        # serialized argument
        cls.serialized_payload = json.dumps(argument_payload)
        # factory models for association.
        cls.location = LocationFactory.create(title="some town")
        cls.registration_import_data = RegistrationDataImportFactory.create(
            name=intake_group
        )
        cls.head_of_household_1 = IndividualFactory.create(
            full_name="John Doe",
            first_name="John",
            last_name="Doe",
            sex="Male",
            dob=dt.date(2000, 3, 3),
        )
        cls.head_of_household_2 = IndividualFactory.create(
            full_name="Jane Doe",
            first_name="Jane",
            last_name="Doe",
            sex="Female",
            dob=dt.date(1996, 3, 3),
        )
        household_to_create = [
            {
                "household_ca_id": "ca_id_1",
                "head_of_household": cls.head_of_household_1,
                "family_size": 5,
                "address": "some street",
                "location": cls.location,
                "registration_data_import_id": cls.registration_import_data,
            },
            {
                "household_ca_id": "ca_id_2",
                "head_of_household": cls.head_of_household_2,
                "family_size": 5,
                "address": "sample street",
                "location": cls.location,
                "registration_data_import_id": cls.registration_import_data,
            },
        ]
        cls.filter_entries = [
            # This is mocked HouseHold Model.
            HouseholdFactory(**data)
            for data in household_to_create
        ]

    def test_filter_query(self):
        self.snapshot_graphql_request(
            request_string=self.FILTER_QUERY,
            context={"user": self.user},
            variables={"serializedList": self.serialized_payload,},
        )


class TestSavedTargetRuleQuery(APITestCase):
    """Gets Saved Snapshots of Target Households Results based on TargetRules."""

    @classmethod
    def setUpTestData(cls):
        # graph query to be called.
        cls.SAVED_TARGET_RULE_QUERY = """
        query SavedTargetRule($id: ID!) {
            savedTargetRule(id: $id) {
                flexRules
                coreRules
                targetPopulation {
                    name
                }
            }
        }
        """
        cls.ALL_SAVED_TARGET_RULE_QUERY = """
        query AllSavedTargetRule {
            allSavedTargetRule {
                edges {
                    node {
                        flexRules
                        coreRules
                        targetPopulation {
                            name
                        }
                    }
                }
            }
        }
        """
        cls.user = UserFactory.create()
        location = LocationFactory.create()
        registration_import_data = RegistrationDataImportFactory.create_batch(5)
        individuals = IndividualFactory.create_batch(5)
        households = HouseholdFactory.create_batch(5)
        for (household, individual, reg) in zip(
            households, individuals, registration_import_data
        ):
            household.head_of_household = individual
            household.registration_data_import_id = reg
            household.location = location
            household.save()

        cls.target_rules = TargetRuleFactory.create_batch(5)
        target_population = TargetPopulationFactory(
            households=households, created_by=cls.user
        )
        target_population.target_rules.add(*cls.target_rules)

    def test_all_saved_target_rule_query(self):
        self.snapshot_graphql_request(
            request_string=self.ALL_SAVED_TARGET_RULE_QUERY,
            context={"user": self.user},
        )

    def test_saved_target_rule_query(self):
        self.snapshot_graphql_request(
            request_string=self.SAVED_TARGET_RULE_QUERY,
            context={"user": self.user},
            variables={
                "id": self.id_to_base64(self.target_rules[0].id, "SavedTargetRule")
            },
        )
