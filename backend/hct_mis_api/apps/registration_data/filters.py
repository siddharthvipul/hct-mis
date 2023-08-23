from django.db.models import QuerySet
from django.db.models.functions import Lower

from django_filters import CharFilter, DateFilter, FilterSet

from hct_mis_api.apps.core.filters import DateTimeRangeFilter, IntegerRangeFilter
from hct_mis_api.apps.core.utils import CustomOrderingFilter, decode_id_string_required
from hct_mis_api.apps.registration_data.models import RegistrationDataImport


class RegistrationDataImportFilter(FilterSet):
    import_date = DateFilter(field_name="import_date__date")
    business_area = CharFilter(field_name="business_area__slug")
    import_date_range = DateTimeRangeFilter(field_name="import_date")
    size = IntegerRangeFilter(field_name="number_of_households")
    program = CharFilter(method="filter_by_program")

    class Meta:
        model = RegistrationDataImport
        fields = {
            "imported_by__id": ["exact"],
            "import_date": ["exact"],
            "status": ["exact"],
            "name": ["exact", "startswith"],
            "business_area": ["exact"],
        }

    order_by = CustomOrderingFilter(
        fields=(
            Lower("name"),
            "status",
            "import_date",
            "number_of_individuals",
            "number_of_households",
            "data_source",
            Lower("imported_by__first_name"),
        )
    )

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        qs = super().filter_queryset(queryset)
        return qs.exclude(excluded=True)

    def filter_by_program(self, queryset: QuerySet, name: str, value: str) -> QuerySet:
        return queryset.filter(program_id=decode_id_string_required(value))
