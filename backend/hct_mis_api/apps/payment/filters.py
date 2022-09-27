from django.db.models import Count, Q, Case, When, Value, CharField, F
from django.db.models.functions import Lower

from django_filters import (
    CharFilter,
    FilterSet,
    OrderingFilter,
    NumberFilter,
    UUIDFilter,
    MultipleChoiceFilter,
    DateFilter,
)
from django.shortcuts import get_object_or_404


from hct_mis_api.apps.activity_log.schema import LogEntryFilter
from hct_mis_api.apps.core.utils import CustomOrderingFilter, is_valid_uuid, decode_id_string
from hct_mis_api.apps.household.models import ROLE_NO_ROLE
from hct_mis_api.apps.payment.models import (
    CashPlan,
    PaymentVerificationPlan,
    FinancialServiceProvider,
    FinancialServiceProviderXlsxReport,
    FinancialServiceProviderXlsxTemplate,
    PaymentRecord,
    PaymentVerification,
    PaymentPlan,
    GenericPayment,
    Payment,
)


class PaymentRecordFilter(FilterSet):
    individual = CharFilter(method="individual_filter")
    business_area = CharFilter(field_name="business_area__slug")

    class Meta:
        fields = (
            "parent",
            "household",
        )
        model = PaymentRecord

    order_by = CustomOrderingFilter(
        fields=(
            "ca_id",
            "status",
            Lower("name"),
            "status_date",
            "cash_assist_id",
            Lower("head_of_household__full_name"),
            "total_person_covered",
            "distribution_modality",
            "household__unicef_id",
            "household__size",
            "entitlement_quantity",
            "delivered_quantity_usd",
            "delivery_date",
        )
    )

    def individual_filter(self, qs, name, value):
        if is_valid_uuid(value):
            return qs.exclude(household__individuals_and_roles__role=ROLE_NO_ROLE)
        return qs


class PaymentVerificationFilter(FilterSet):
    search = CharFilter(method="search_filter")
    business_area = CharFilter(field_name="payment_record__business_area__slug")
    verification_channel = CharFilter(field_name="payment_verification_plan__verification_channel")

    class Meta:
        fields = ("payment_verification_plan", "status")  # TODO: add 'payment_verification_plan__payment_plan'
        model = PaymentVerification

    order_by = OrderingFilter(
        fields=(
            "payment_record__ca_id",
            "payment_verification_plan__verification_channel",
            "payment_verification_plan__unicef_id",
            "status",
            "payment_record__head_of_household__family_name",
            "payment_record__household__unicef_id",
            "payment_record__household__status",
            "payment_record__delivered_quantity",
            "received_amount",
            "payment_record__head_of_household__phone_no",
            "payment_record__head_of_household__phone_no_alternative",
        )
    )

    def search_filter(self, qs, name, value):
        values = value.split(" ")
        q_obj = Q()
        for value in values:
            q_obj |= Q(payment_record__ca_id__istartswith=value)
            q_obj |= Q(payment_verification_plan__unicef_id__istartswith=value)
            q_obj |= Q(received_amount__istartswith=value)
            q_obj |= Q(payment_record__household__unicef_id__istartswith=value)
            q_obj |= Q(payment_record__head_of_household__full_name__istartswith=value)
            q_obj |= Q(payment_record__head_of_household__given_name__istartswith=value)
            q_obj |= Q(payment_record__head_of_household__middle_name__istartswith=value)
            q_obj |= Q(payment_record__head_of_household__family_name__istartswith=value)
            q_obj |= Q(payment_record__head_of_household__phone_no__istartswith=value)
            q_obj |= Q(payment_record__head_of_household__phone_no_alternative__istartswith=value)
        return qs.filter(q_obj)


class PaymentVerificationPlanFilter(FilterSet):
    class Meta:
        fields = tuple()
        model = PaymentVerificationPlan


class PaymentVerificationLogEntryFilter(LogEntryFilter):
    object_id = UUIDFilter(method="object_id_filter")

    def object_id_filter(self, qs, name, value):
        cash_plan = CashPlan.objects.get(pk=value)
        verifications_ids = cash_plan.payment_verification_plans.all().values_list("pk", flat=True)
        return qs.filter(object_id__in=verifications_ids)


class FinancialServiceProviderXlsxTemplateFilter(FilterSet):
    class Meta:
        fields = (
            "name",
            "created_by",
        )
        model = FinancialServiceProviderXlsxTemplate

    order_by = CustomOrderingFilter(
        fields=(
            Lower("name"),
            "created_by",
        )
    )


class FinancialServiceProviderXlsxReportFilter(FilterSet):
    class Meta:
        fields = ("status",)
        model = FinancialServiceProviderXlsxReport

    order_by = CustomOrderingFilter(fields=("status",))


class FinancialServiceProviderFilter(FilterSet):
    delivery_mechanisms = MultipleChoiceFilter(
        field_name="delivery_mechanisms", choices=GenericPayment.DELIVERY_TYPE_CHOICE
    )

    class Meta:
        fields = (
            "created_by",
            "name",
            "vision_vendor_number",
            "delivery_mechanisms",
            "distribution_limit",
            "communication_channel",
            "fsp_xlsx_template",
        )
        model = FinancialServiceProvider

    order_by = CustomOrderingFilter(
        fields=(
            "id",
            Lower("name"),
            "vision_vendor_number",
            "delivery_mechanisms",
            "distribution_limit",
            "communication_channel",
        )
    )


class CashPlanFilter(FilterSet):
    search = CharFilter(method="search_filter")
    delivery_type = MultipleChoiceFilter(field_name="delivery_type", choices=PaymentRecord.DELIVERY_TYPE_CHOICE)
    verification_status = MultipleChoiceFilter(
        field_name="payment_verification_summary__status", choices=PaymentVerificationPlan.STATUS_CHOICES
    )
    business_area = CharFilter(
        field_name="business_area__slug",
    )

    class Meta:
        fields = {
            "program": ["exact"],
            "assistance_through": ["exact", "startswith"],
            "service_provider__full_name": ["exact", "startswith"],
            "start_date": ["exact", "lte", "gte"],
            "end_date": ["exact", "lte", "gte"],
            "business_area": ["exact"],
        }
        model = CashPlan

    order_by = OrderingFilter(
        fields=(
            "ca_id",
            "status",
            "total_number_of_hh",
            "total_entitled_quantity",
            ("payment_verification_summary__status", "verification_status"),
            "total_persons_covered",
            "total_delivered_quantity",
            "total_undelivered_quantity",
            "dispersion_date",
            "assistance_measurement",
            "assistance_through",
            "delivery_type",
            "start_date",
            "end_date",
            "program__name",
            "id",
            "updated_at",
            "service_provider__full_name",
        )
    )

    def filter_queryset(self, queryset):
        queryset = queryset.annotate(total_number_of_hh=Count("payment_items"))
        return super().filter_queryset(queryset)

    def search_filter(self, qs, name, value):
        values = value.split(" ")
        q_obj = Q()
        for value in values:
            q_obj |= Q(ca_id__istartswith=value)
        return qs.filter(q_obj)


class PaymentPlanFilter(FilterSet):
    business_area = CharFilter(field_name="business_area__slug", required=True)
    search = CharFilter(method="search_filter")
    status = MultipleChoiceFilter(field_name="status", choices=PaymentPlan.Status.choices)
    total_entitled_quantity_from = NumberFilter(field_name="total_entitled_quantity", lookup_expr="gte")
    total_entitled_quantity_to = NumberFilter(field_name="total_entitled_quantity", lookup_expr="lte")
    dispersion_start_date = DateFilter(field_name="dispersion_start_date", lookup_expr="gte")
    dispersion_end_date = DateFilter(field_name="dispersion_end_date", lookup_expr="lte")

    class Meta:
        fields = tuple()
        model = PaymentPlan

    def filter_queryset(self, queryset):
        queryset = queryset.annotate(total_number_of_hh=Count("payment_items"))
        if not self.form.cleaned_data.get("order_by"):
            queryset = queryset.order_by("unicef_id")
        return super().filter_queryset(queryset)

    order_by = OrderingFilter(
        fields=(
            "unicef_id",
            "status",
            "total_households_count",
            "currency",
            "total_entitled_quantity",
            "total_delivered_quantity",
            "total_undelivered_quantity",
            "dispersion_start_date",
            "dispersion_end_date",
            "created_at",
        )
    )

    def search_filter(self, qs, name, value):
        return qs.filter(Q(id__icontains=value) | Q(unicef_id__icontains=value))


class PaymentFilter(FilterSet):
    business_area = CharFilter(field_name="parent__business_area__slug", required=True)
    payment_plan_id = CharFilter(required=True, method="payment_plan_id_filter")

    def payment_plan_id_filter(self, qs, name, value):
        payment_plan_id = decode_id_string(value)
        payment_plan = get_object_or_404(PaymentPlan, id=payment_plan_id)
        q = Q(parent=payment_plan)
        if payment_plan.status != PaymentPlan.Status.OPEN:
            q &= ~Q(excluded=True)
        return qs.filter(q)

    class Meta:
        fields = tuple()
        model = Payment

    order_by = OrderingFilter(
        fields=(
            "unicef_id",
            "status",
            "household_id",
            "household__size",
            "admin2",
            "collector_id",
            "assigned_payment_channel",
            "entitlement_quantity_usd",
            "delivered_quantity",
        )
    )

    def filter_queryset(self, queryset):
        # household__admin2
        queryset = queryset.annotate(
            admin2=Case(
                When(
                    household__admin_area__isnull=True,
                    then=Value(""),
                ),
                When(
                    household__admin_area__isnull=False,
                    household__admin_area__area_type__area_level__in=(0, 1),
                    then=Value(""),
                ),
                When(
                    household__admin_area__isnull=False,
                    household__admin_area__area_type__area_level__lt=2,
                    household__admin_area__area_type__area_level__gt=2,
                    then=Lower("household__admin_area__parent__name"),
                ),
                When(
                    household__admin_area__isnull=False,
                    then=Lower("household__admin_area__name"),
                ),
                default=Value(""),
                output_field=CharField(),
            )
        )
        if not self.form.cleaned_data.get("order_by"):
            queryset = queryset.order_by("unicef_id")

        return super().filter_queryset(queryset)


# TODO need update this one
class CashPlanPaymentPlanFilter(FilterSet):
    business_area = CharFilter(field_name="business_area__slug", required=True)

    class Meta:
        model = CashPlan
        fields = tuple()

    order_by = OrderingFilter(
        fields=(
            "unicef_id",
        )
    )
