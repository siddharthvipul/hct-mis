from django.core.management import call_command
from parameterized import parameterized

from account.fixtures import UserFactory
from account.permissions import Permissions
from core.base_test_case import APITestCase
from core.fixtures import AdminAreaTypeFactory, AdminAreaFactory
from core.models import BusinessArea
from grievance.models import GrievanceTicket


class TestGrievanceCreateFeedbackTicketQuery(APITestCase):
    CREATE_GRIEVANCE_MUTATION = """
    mutation CreateGrievanceTicket($input: CreateGrievanceTicketInput!) {
      createGrievanceTicket(input: $input) {
        grievanceTickets{
          category
          admin
          language
          description
          consent
        }
      }
    }
    """

    def setUp(self):
        super().setUp()
        call_command("loadbusinessareas")
        self.user = UserFactory.create()
        self.business_area = BusinessArea.objects.get(slug="afghanistan")
        area_type = AdminAreaTypeFactory(
            name="Admin type one",
            admin_level=2,
            business_area=self.business_area,
        )
        self.admin_area = AdminAreaFactory(title="City Test", admin_area_type=area_type)

    @parameterized.expand(
        [
            (
                "with_permission",
                [Permissions.GRIEVANCES_CREATE],
            ),
            ("without_permission", []),
        ]
    )
    def test_create_positive_feedback_ticket(self, _, permissions):
        self.create_user_role_with_permissions(self.user, permissions, self.business_area)

        input_data = {
            "input": {
                "description": "Test Feedback",
                "assignedTo": self.id_to_base64(self.user.id, "UserNode"),
                "category": GrievanceTicket.CATEGORY_POSITIVE_FEEDBACK,
                "admin": self.admin_area.title,
                "language": "Polish, English",
                "consent": True,
                "businessArea": "afghanistan",
            }
        }

        self.snapshot_graphql_request(
            request_string=self.CREATE_GRIEVANCE_MUTATION,
            context={"user": self.user},
            variables=input_data,
        )
