import pytest
from page_object.grievance.grievance_dashboard import GrievanceDashboard

from hct_mis_api.apps.account.models import User
from hct_mis_api.apps.core.models import BusinessArea
from hct_mis_api.apps.grievance.models import GrievanceTicket
from hct_mis_api.apps.program.models import Program
from selenium_tests.helpers.fixtures import get_program_with_dct_type_and_name

pytestmark = pytest.mark.django_db(transaction=True)


@pytest.fixture
def active_program() -> Program:
    return get_program_with_dct_type_and_name("Test Program", "1234")


@pytest.fixture
def add_grievances() -> None:
    GrievanceTicket._meta.get_field("created_at").auto_now_add = False
    GrievanceTicket._meta.get_field("updated_at").auto_now = False
    for i in range(50):
        generate_grievance(f"GRV-000000{i}")
    for i in range(10):
        generate_grievance(
            f"GRV-00000{i + 50}",
            category=GrievanceTicket.CATEGORY_NEEDS_ADJUDICATION,
        )
    for i in range(25):
        generate_grievance(
            f"GRV-00000{i + 60}",
            created_at="2022-09-27T11:26:33.846Z",
            updated_at="2023-09-27T11:26:33.846Z",
            status=GrievanceTicket.STATUS_CLOSED,
        )
    for i in range(15):
        generate_grievance(
            f"GRV-0000{i + 100}",
            status=GrievanceTicket.STATUS_CLOSED,
            category=GrievanceTicket.CATEGORY_NEEDS_ADJUDICATION,
        )
    GrievanceTicket._meta.get_field("created_at").auto_now_add = True


def generate_grievance(
    unicef_id: str,
    status: int = GrievanceTicket.STATUS_NEW,
    category: int = GrievanceTicket.CATEGORY_POSITIVE_FEEDBACK,
    created_by: User | None = None,
    assigned_to: User | None = None,
    business_area: BusinessArea | None = None,
    priority: int = 1,
    urgency: int = 1,
    household_unicef_id: str = "HH-20-0000.0001",
    updated_at: str = "2023-09-27T11:26:33.846Z",
    created_at: str = "2022-04-30T09:54:07.827000",
) -> None:
    created_by = User.objects.first() if created_by is None else created_by
    assigned_to = User.objects.first() if assigned_to is None else assigned_to
    business_area = BusinessArea.objects.filter(slug="afghanistan").first() if business_area is None else business_area
    GrievanceTicket.objects.create(
        **{
            "business_area": business_area,
            "unicef_id": unicef_id,
            "language": "Polish",
            "consent": True,
            "description": "grievance_ticket_1",
            "category": category,
            "status": status,
            "created_by": created_by,
            "assigned_to": assigned_to,
            "created_at": created_at,
            "updated_at": updated_at,
            "household_unicef_id": household_unicef_id,
            "priority": priority,
            "urgency": urgency,
        }
    )


@pytest.mark.usefixtures("login")
class TestSmokeGrievanceDashboard:
    def test_smoke_grievance_dashboard(
        self,
        active_program: Program,
        add_grievances: None,
        pageGrievanceDashboard: GrievanceDashboard,
    ) -> None:
        pageGrievanceDashboard.getNavGrievance().click()
        pageGrievanceDashboard.getNavGrievanceDashboard().click()

        assert "Grievance Dashboard" in pageGrievanceDashboard.getPageHeaderTitle().text
        assert "100" in pageGrievanceDashboard.getTotalNumberOfTicketsTopNumber().text
        assert "25" in pageGrievanceDashboard.getLabelizedFieldContainerTotalNumberOfTicketsSystemGenerated().text
        assert "75" in pageGrievanceDashboard.getLabelizedFieldContainerTotalNumberOfTicketsUserGenerated().text
        assert "40" in pageGrievanceDashboard.getTotalNumberOfClosedTicketsTopNumber().text
        assert "15" in pageGrievanceDashboard.getLabelizedFieldContainerTotalNumberOfClosedTicketsSystemGenerated().text
        assert "25" in pageGrievanceDashboard.getLabelizedFieldContainerTotalNumberOfClosedTicketsUserGenerated().text
        assert "421.25 days" in pageGrievanceDashboard.getTicketsAverageResolutionTopNumber().text
        assert (
            "515 days"
            in pageGrievanceDashboard.getLabelizedFieldContainerTicketsAverageResolutionSystemGenerated().text
        )
        assert (
            "365 days" in pageGrievanceDashboard.getLabelizedFieldContainerTicketsAverageResolutionUserGenerated().text
        )
        GrievanceTicket._meta.get_field("updated_at").auto_now = True
