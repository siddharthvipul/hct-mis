from django.test import TestCase

from hct_mis_api.apps.core.fixtures import create_afghanistan
from hct_mis_api.apps.household.fixtures import IndividualRoleInHouseholdFactory, create_household_and_individuals
from hct_mis_api.apps.household.models import ROLE_PRIMARY, ROLE_ALTERNATE, IndividualRoleInHousehold
from hct_mis_api.one_time_scripts.handle_individuals_with_multiple_roles import update_individuals_with_multiple_roles


class TestHandleIndividualsWithMultipleRoles(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        business_area = create_afghanistan()
        cls.household, cls.individual = create_household_and_individuals(
            household_data={"size": 1, "business_area": business_area},
            individuals_data=[{}],
        )
        IndividualRoleInHouseholdFactory(household=cls.household, individual=cls.individual[0], role=ROLE_PRIMARY)
        IndividualRoleInHouseholdFactory(household=cls.household, individual=cls.individual[0], role=ROLE_ALTERNATE)

    def test_handle_individuals_with_multiple_roles_within_household(self) -> None:
        roles = IndividualRoleInHousehold.objects.filter(household=self.household, individual=self.individual[0]).count()
        self.assertEqual(roles, 2)
        update_individuals_with_multiple_roles()
        roles = IndividualRoleInHousehold.objects.filter(household=self.household, individual=self.individual[0]).count()
        self.assertEqual(roles, 1)
