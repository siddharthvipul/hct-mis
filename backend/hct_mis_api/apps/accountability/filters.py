import re

from django.db.models import Q, QuerySet
from django.db.models.functions import Lower

from django_filters import CharFilter, ChoiceFilter, FilterSet, UUIDFilter

from hct_mis_api.apps.accountability.models import (
    Feedback,
    FeedbackMessage,
    Message,
    Survey,
)
from hct_mis_api.apps.core.filters import DateTimeRangeFilter
from hct_mis_api.apps.core.utils import CustomOrderingFilter, decode_id_string
from hct_mis_api.apps.household.models import Household


class MessagesFilter(FilterSet):
    program = CharFilter(method="filter_program")
    created_at_range = DateTimeRangeFilter(field_name="created_at")
    title = CharFilter(field_name="title", lookup_expr="icontains")
    body = CharFilter(field_name="body", lookup_expr="icontains")
    sampling_type = ChoiceFilter(field_name="sampling_type", choices=Message.SamplingChoices.choices)

    def filter_program(self, queryset: QuerySet, name: str, value: str) -> QuerySet[Message]:
        return queryset.filter(target_population__program=decode_id_string(value))

    class Meta:
        model = Message
        fields = {
            "number_of_recipients": ["exact", "gte", "lte"],
            "target_population": ["exact"],
            "created_by": ["exact"],
        }

    order_by = CustomOrderingFilter(
        fields=(Lower("title"), "number_of_recipients", "sampling_type", "created_by", "id", "created_at")
    )


class MessageRecipientsMapFilter(FilterSet):
    message_id = CharFilter(method="filter_message_id", required=True)
    recipient_id = CharFilter(method="filter_recipient_id")
    full_name = CharFilter(field_name="head_of_household__full_name", lookup_expr=["exact", "icontains", "istartswith"])
    phone_no = CharFilter(field_name="head_of_household__phone_no", lookup_expr=["exact", "icontains", "istartswith"])
    sex = CharFilter(field_name="head_of_household__sex")

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        queryset = queryset.exclude(
            head_of_household__phone_no_valid=False, head_of_household__phone_no_alternative_valid=False
        )
        return super().filter_queryset(queryset)

    def filter_message_id(self, queryset: QuerySet, name: str, value: str) -> QuerySet[Household]:
        return queryset.filter(messages__id=decode_id_string(value))

    def filter_recipient_id(self, queryset: QuerySet, name: str, value: str) -> QuerySet[Household]:
        return queryset.filter(head_of_household_id=decode_id_string(value))

    class Meta:
        model = Household
        fields = []

    order_by = CustomOrderingFilter(
        fields=(
            "id",
            "unicef_id",
            "withdrawn",
            Lower("head_of_household__full_name"),
            Lower("head_of_household__sex"),
            "size",
            Lower("admin_area__name"),
            "residence_status",
            "head_of_household__first_registration_date",
        )
    )


class FeedbackFilter(FilterSet):
    issue_type = ChoiceFilter(field_name="issue_type", choices=Feedback.ISSUE_TYPE_CHOICES)
    created_at_range = DateTimeRangeFilter(field_name="created_at")
    created_by = CharFilter(method="filter_created_by")
    feedback_id = CharFilter(method="filter_feedback_id")

    def filter_created_by(self, queryset: QuerySet, name: str, value: str) -> QuerySet[Feedback]:
        return queryset.filter(created_by__pk=value)

    def filter_feedback_id(self, queryset: QuerySet, name: str, value: str) -> QuerySet[Feedback]:
        return queryset.filter(unicef_id=value)

    class Meta:
        model = Feedback
        fields = ()

    order_by = CustomOrderingFilter(
        fields=(
            "unicef_id",
            "issue_type",
            "household_lookup",
            "created_by",
            "created_at",
            "linked_grievance",
        )
    )


class FeedbackMessageFilter(FilterSet):
    feedback = UUIDFilter(field_name="feedback", required=True)

    class Meta:
        fields = ("id",)
        model = FeedbackMessage


class SurveyFilter(FilterSet):
    created_at_range = DateTimeRangeFilter(field_name="created_at")
    search = CharFilter(method="filter_search")

    def filter_search(self, queryset: QuerySet, name: str, value: str) -> QuerySet[Survey]:
        if re.match(r"([\"\']).+\1", value):
            values = [value.replace('"', "").strip()]
        else:
            values = value.split(" ")
        q_obj = Q()
        for value in values:
            value = value.strip(",")
            inner_query = Q()
            inner_query |= Q(title__icontains=value)
            inner_query |= Q(unicef_id__istartswith=value)
            inner_query |= Q(unicef_id__iendswith=value)

            q_obj &= inner_query
        return queryset.filter(q_obj).distinct()

    class Meta:
        model = Survey
        fields = {
            "program": ["exact"],
            "target_population": ["exact"],
            "created_by": ["exact"],
        }

    order_by = CustomOrderingFilter(
        fields=(
            "unicef_id",
            "title",
            "category",
            "number_of_recipient",
            "created_by",
            "created_at",
        )
    )


class RecipientFilter(FilterSet):
    survey = CharFilter(method="filter_survey", required=True)

    class Meta:
        model = Household
        fields = []

    order_by = CustomOrderingFilter(
        fields=(
            "unicef_id",
            "head_of_household__full_name",
            "size",
            "admin_area__name",
            "residence_status",
            "registered_at",
        )
    )

    def filter_survey(self, queryset: QuerySet, name: str, value: str) -> QuerySet[Household]:
        return queryset.filter(surveys__id=decode_id_string(value))