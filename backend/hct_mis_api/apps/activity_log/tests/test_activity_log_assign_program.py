from django.core.management import call_command

from hct_mis_api.apps.account.fixtures import UserFactory
from hct_mis_api.apps.activity_log.models import LogEntry
from hct_mis_api.apps.core.base_test_case import APITestCase
from hct_mis_api.apps.core.fixtures import create_afghanistan
from hct_mis_api.apps.core.models import BusinessArea
from hct_mis_api.apps.grievance.fixtures import GrievanceTicketFactory
from hct_mis_api.apps.payment.fixtures import (
    CashPlanFactory,
    PaymentFactory,
    PaymentPlanFactory,
    PaymentVerificationFactory,
    PaymentVerificationPlanFactory,
    PaymentVerificationSummaryFactory,
)
from hct_mis_api.apps.program.fixtures import ProgramCycleFactory, ProgramFactory
from hct_mis_api.apps.registration_data.fixtures import RegistrationDataImportFactory
from hct_mis_api.apps.targeting.fixtures import TargetPopulationFactory


class TestLogsAssignProgram(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        create_afghanistan()
        business_area = BusinessArea.objects.get(slug="afghanistan")
        user = UserFactory(first_name="User", last_name="WithLastName")

        cls.program = ProgramFactory(business_area=business_area)
        program_cycle = ProgramCycleFactory(program=cls.program, iteration=2)

        rdi = RegistrationDataImportFactory(business_area=business_area, program_id=cls.program.pk)
        tp = TargetPopulationFactory(program=cls.program, business_area=business_area)
        payment_plan = PaymentPlanFactory(business_area=business_area, program=cls.program, program_cycle=program_cycle)
        payment = PaymentFactory(parent=payment_plan, business_area=business_area)
        cash_plan = CashPlanFactory(business_area=business_area, program=cls.program)
        PaymentVerificationSummaryFactory(generic_fk_obj=payment_plan)
        payment_verification_plan = PaymentVerificationPlanFactory(payment_plan_obj=payment_plan)
        payment_verification = PaymentVerificationFactory(
            payment_verification_plan=payment_verification_plan, generic_fk_obj=payment
        )
        grievance_ticket = GrievanceTicketFactory(business_area=business_area, programme=cls.program)
        # TODO: update after changes for Ind and HH collections/representations
        # individual = IndividualFactory(household=None, program=cls.program)
        # household = HouseholdFactory(head_of_household=individual, program=cls.program)

        # log for Program
        LogEntry.objects.create(
            action=LogEntry.CREATE,
            content_object=cls.program,
            user=user,
            program=None,
            business_area=business_area,
            object_repr=str(cls.program),
            changes=dict(),
        )
        # log for RegistrationDataImport
        LogEntry.objects.create(
            action=LogEntry.CREATE,
            content_object=rdi,
            user=user,
            program=None,
            business_area=business_area,
            object_repr=str(rdi),
            changes=dict(),
        )
        # log for TargetPopulation
        LogEntry.objects.create(
            action=LogEntry.CREATE,
            content_object=tp,
            user=user,
            program=None,
            business_area=business_area,
            object_repr=str(tp),
            changes=dict(),
        )
        # log for PaymentPlan
        LogEntry.objects.create(
            action=LogEntry.CREATE,
            content_object=payment_plan,
            user=user,
            program=None,
            business_area=business_area,
            object_repr=str(payment_plan),
            changes=dict(),
        )
        # log for CashPlan
        LogEntry.objects.create(
            action=LogEntry.CREATE,
            content_object=cash_plan,
            user=user,
            program=None,
            business_area=business_area,
            object_repr=str(cash_plan),
            changes=dict(),
        )
        # log for PaymentVerificationPlan
        LogEntry.objects.create(
            action=LogEntry.CREATE,
            content_object=payment_verification_plan,
            user=user,
            program=None,
            business_area=business_area,
            object_repr=str(payment_verification_plan),
            changes=dict(),
        )
        # log for PaymentVerification
        LogEntry.objects.create(
            action=LogEntry.CREATE,
            content_object=payment_verification,
            user=user,
            program=None,
            business_area=business_area,
            object_repr=str(payment_verification),
            changes=dict(),
        )
        # log for GrievanceTicket
        LogEntry.objects.create(
            action=LogEntry.CREATE,
            content_object=grievance_ticket,
            user=user,
            program=None,
            business_area=business_area,
            object_repr=str(grievance_ticket),
            changes=dict(),
        )
        # TODO: update after changes for Ind and HH collections/representations
        # # log for Individual
        # LogEntry.objects.create(
        #     action=LogEntry.CREATE,
        #     content_object=individual,
        #     user=user,
        #     program=None,
        #     business_area=business_area,
        #     object_repr=str(individual),
        #     changes=dict(),
        # )
        # # log for Household
        # LogEntry.objects.create(
        #     action=LogEntry.CREATE,
        #     content_object=household,
        #     user=user,
        #     program=None,
        #     business_area=business_area,
        #     object_repr=str(household),
        #     changes=dict(),
        # )

    def test_assign_program_to_existing_logs(self) -> None:
        assert LogEntry.objects.filter(program__isnull=True).count() == 8

        call_command("activity_log_assign_program")

        print("==> ", LogEntry.objects.filter(program__isnull=True).count())
        assert LogEntry.objects.filter(program__isnull=True).count() == 0
        assert LogEntry.objects.filter(program_id=self.program.pk).count() == 8

        program_uuid = "dfef92b5-472c-478c-91df-53deb79a704a"
        ba = BusinessArea.objects.get(slug="afghanistan")
        user = UserFactory()
        rdi = RegistrationDataImportFactory(business_area=ba, program_id=program_uuid)
        rdi_log = LogEntry.objects.create(
            action=LogEntry.CREATE,
            content_object=rdi,
            user=user,
            program=None,
            business_area=ba,
            object_repr=str(rdi),
            changes=dict(),
        )
        LogEntry.objects.create(
            action=LogEntry.CREATE,
            content_object=user,
            user=user,
            program=None,
            business_area=ba,
            object_repr=str(user),
            changes=dict(),
        )

        with self.assertRaisesMessage(ValueError, "Can not found 'class_name' and 'nested_field' for class User"):
            call_command("activity_log_assign_program")

        # check transaction.atomic
        rdi_log.refresh_from_db()
        assert rdi_log.program is None
