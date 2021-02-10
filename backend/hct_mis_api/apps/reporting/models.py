from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _

from hct_mis_api.apps.utils.models import TimeStampedUUIDModel
from hct_mis_api.apps.account.models import ChoiceArrayField


class Report(TimeStampedUUIDModel):
    IN_PROGRESS = 1
    COMPLETED = 2
    FAILED = 3
    STATUSES = ((IN_PROGRESS, _("Processing")), (COMPLETED, _("Generated")), (FAILED, _("Failed")))

    INDIVIDUALS = 1
    HOUSEHOLD_DEMOGRAPHICS = 2
    CASH_PLAN_VERIFICATION = 3
    PAYMENTS = 4
    PAYMENT_VERIFICATION = 5
    CASH_PLAN = 6
    PROGRAM = 7
    INDIVIDUALS_AND_PAYMENT = 8
    REPORT_TYPES = (
        (INDIVIDUALS, _("Individuals")),
        (HOUSEHOLD_DEMOGRAPHICS, _("Households")),
        (CASH_PLAN_VERIFICATION, _("Cash Plan Verification")),
        (PAYMENTS, _("Payments")),
        (PAYMENT_VERIFICATION, _("Payment verification")),
        (CASH_PLAN, _("Cash Plan")),
        (PROGRAM, _("Programme")),
        (INDIVIDUALS_AND_PAYMENT, _("Individuals & Payment")),
    )

    business_area = models.ForeignKey("core.BusinessArea", related_name="reports", on_delete=models.CASCADE)
    file = models.FileField(blank=True, null=True)
    created_by = models.ForeignKey("account.User", related_name="reports", on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUSES, default=IN_PROGRESS)
    report_type = models.IntegerField(choices=REPORT_TYPES)
    date_from = models.DateField()
    date_to = models.DateField()
    number_of_records = models.IntegerField(blank=True, null=True)
    # any of these are optional and their requirements will depend on report type
    program = models.ForeignKey(
        "program.Program", on_delete=models.CASCADE, blank=True, null=True, related_name="reports"
    )
    admin_area = models.ManyToManyField("core.AdminArea", blank=True, related_name="reports")

    def __str__(self):
        return f"[{self.report_type}] Report for [{self.business_area}]"

    class Meta:
        ordering = ["-created_at", "report_type", "status", "created_by"]


class DashboardReport(TimeStampedUUIDModel):
    IN_PROGRESS = 1
    COMPLETED = 2
    FAILED = 3
    STATUSES = ((IN_PROGRESS, _("Processing")), (COMPLETED, _("Generated")), (FAILED, _("Failed")))

    TOTAL_TRANSFERRED_BY_COUNTRY = 1
    TOTAL_TRANSFERRED_BY_ADMIN_AREA = 2
    BENEFICIARIES_REACHED = 3
    INDIVIDUALS_REACHED = 4
    VOLUME_BY_DELIVERY_MECHANISM = 5
    GRIEVANCES_AND_FEEDBACK = 6
    PROGRAMS = 7
    PAYMENT_VERIFICATION = 8
    REPORT_TYPES = (
        (TOTAL_TRANSFERRED_BY_COUNTRY, _("Total transferred by country")),
        (TOTAL_TRANSFERRED_BY_ADMIN_AREA, _("Total transferred by administrative area")),
        (BENEFICIARIES_REACHED, _("Beneficiaries reached")),
        (INDIVIDUALS_REACHED, _("Individuals reached drilldown")),
        (VOLUME_BY_DELIVERY_MECHANISM, _("Volume by delivery mechanism")),
        (GRIEVANCES_AND_FEEDBACK, _("Grievances and Feedback")),
        (PROGRAMS, _("Programmes")),
        (PAYMENT_VERIFICATION, _("Payment verification")),
    )

    business_area = models.ForeignKey("core.BusinessArea", related_name="dashboard_reports", on_delete=models.CASCADE)
    file = models.FileField(blank=True, null=True)
    created_by = models.ForeignKey("account.User", related_name="dashboard_reports", on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(choices=STATUSES, default=IN_PROGRESS)
    report_type = ChoiceArrayField(models.PositiveSmallIntegerField(choices=REPORT_TYPES))

    # filters
    year = models.PositiveSmallIntegerField(default=datetime.now().year)
    program = models.ForeignKey(
        "program.Program", on_delete=models.CASCADE, blank=True, null=True, related_name="dashboard_reports"
    )
    admin_area = models.ForeignKey(
        "core.AdminArea", on_delete=models.CASCADE, blank=True, null=True, related_name="dashboard_reports"
    )
