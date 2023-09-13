from typing import Any, Dict, List, Optional

from django.conf import settings
from django.contrib.postgres.fields import CICharField
from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    ProhibitNullCharactersValidator,
)
from django.db import models
from django.db.models import Q
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from hct_mis_api.apps.activity_log.utils import create_mapping_dict
from hct_mis_api.apps.core.models import BusinessArea
from hct_mis_api.apps.registration_datahub.models import ImportedIndividual
from hct_mis_api.apps.utils.models import ConcurrencyModel, TimeStampedUUIDModel
from hct_mis_api.apps.utils.validators import (
    DoubleSpaceValidator,
    StartEndSpaceValidator,
)


class RegistrationDataImport(TimeStampedUUIDModel, ConcurrencyModel):
    ACTIVITY_LOG_MAPPING = create_mapping_dict(
        [
            "name",
            "status",
            "import_date",
            "imported_by",
            "data_source",
            "number_of_individuals",
            "number_of_households",
            "datahub_id",
            "error_message",
        ]
    )
    LOADING = "LOADING"
    IMPORT_SCHEDULED = "IMPORT_SCHEDULED"
    IMPORTING = "IMPORTING"
    IN_REVIEW = "IN_REVIEW"
    MERGE_SCHEDULED = "MERGE_SCHEDULED"
    MERGING = "MERGING"
    MERGED = "MERGED"
    DEDUPLICATION_FAILED = "DEDUPLICATION_FAILED"
    DEDUPLICATION = "DEDUPLICATION"
    REFUSED_IMPORT = "REFUSED"
    IMPORT_ERROR = "IMPORT_ERROR"
    MERGE_ERROR = "MERGE_ERROR"
    STATUS_CHOICE = (
        (LOADING, _("Loading")),
        (DEDUPLICATION, _("Deduplication")),
        (DEDUPLICATION_FAILED, _("Deduplication Failed")),
        (IMPORT_SCHEDULED, _("Import Scheduled")),
        (IMPORTING, _("Importing")),
        (IMPORT_ERROR, _("Import Error")),
        (IN_REVIEW, _("In Review")),
        (MERGE_SCHEDULED, _("Merge Scheduled")),
        (MERGED, _("Merged")),
        (MERGING, _("Merging")),
        (MERGE_ERROR, _("Merge Error")),
        (REFUSED_IMPORT, _("Refused import")),
    )
    XLS = "XLS"
    KOBO = "KOBO"
    DIIA = "DIIA"
    API = "API"
    FLEX_REGISTRATION = "FLEX_REGISTRATION"
    EDOPOMOGA = "EDOPOMOGA"
    DATA_SOURCE_CHOICE = (
        (XLS, "Excel"),
        (KOBO, "KoBo"),
        (DIIA, "DIIA"),
        (FLEX_REGISTRATION, "Flex Registration"),
        (API, "Flex API"),
        (EDOPOMOGA, "eDopomoga"),
    )
    name = CICharField(
        max_length=255,
        unique=True,
        db_index=True,
        validators=[
            MinLengthValidator(3),
            MaxLengthValidator(255),
            DoubleSpaceValidator,
            StartEndSpaceValidator,
            ProhibitNullCharactersValidator(),
        ],
    )
    status = models.CharField(max_length=255, choices=STATUS_CHOICE, default=IN_REVIEW, db_index=True)
    import_date = models.DateTimeField(auto_now_add=True, db_index=True)
    imported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="registration_data_imports",
        on_delete=models.CASCADE,
        null=True,
    )
    data_source = models.CharField(
        max_length=255,
        choices=DATA_SOURCE_CHOICE,
    )
    number_of_individuals = models.PositiveIntegerField(db_index=True)
    number_of_households = models.PositiveIntegerField(db_index=True)

    batch_duplicates = models.PositiveIntegerField(default=0)
    batch_possible_duplicates = models.PositiveIntegerField(default=0)
    batch_unique = models.PositiveIntegerField(default=0)
    golden_record_duplicates = models.PositiveIntegerField(default=0)
    golden_record_possible_duplicates = models.PositiveIntegerField(default=0)
    golden_record_unique = models.PositiveIntegerField(default=0)

    datahub_id = models.UUIDField(null=True, default=None, db_index=True, blank=True)
    error_message = models.TextField(blank=True)
    sentry_id = models.CharField(max_length=100, default="", blank=True, null=True)

    pull_pictures = models.BooleanField(default=True)
    business_area = models.ForeignKey(BusinessArea, null=True, on_delete=models.CASCADE)
    screen_beneficiary = models.BooleanField(default=False)
    excluded = models.BooleanField(default=False, help_text="Exclude RDI in UI")
    # TODO: in future will use one program per RDI after migration
    program = models.ForeignKey(
        "program.Program",
        null=True,
        blank=True,
        db_index=True,
        related_name="registration_imports",
        on_delete=models.SET_NULL,
    )
    programs = models.ManyToManyField(
        "program.Program",
        related_name="registration_data_imports",
    )
    erased = models.BooleanField(default=False, help_text="Abort RDI")
    refuse_reason = models.CharField(max_length=100, blank=True, null=True)
    # TODO: in future will use one program per RDI after migration
    program = models.ForeignKey(
        "program.Program",
        null=True,
        blank=True,
        db_index=True,
        related_name="registration_imports",
        on_delete=models.SET_NULL,
    )
    programs = models.ManyToManyField(
        "program.Program",
        related_name="registration_data_imports",
    )

    def __str__(self) -> str:
        return self.name

    @cached_property
    def all_imported_individuals(self) -> models.QuerySet[ImportedIndividual]:
        return ImportedIndividual.objects.filter(registration_data_import=self.datahub_id)

    class Meta:
        unique_together = ("name", "business_area")
        verbose_name = "Registration data import"

    def should_check_against_sanction_list(self) -> bool:
        return self.screen_beneficiary

    @classmethod
    def get_choices(
        cls, business_area_slug: Optional[str] = None, program_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        query = ~Q(status__in=[cls.DEDUPLICATION_FAILED, cls.MERGE_ERROR, cls.IMPORT_ERROR, cls.REFUSED_IMPORT])
        if business_area_slug:
            query &= Q(business_area__slug=business_area_slug)
        if program_id:
            query &= Q(program_id=program_id)
        queryset = cls.objects.filter(query)
        return [
            {
                "label": {"English(EN)": f"{rdi.name}"},
                "value": rdi.id,
            }
            for rdi in queryset
        ]

    def can_be_merged(self) -> bool:
        return self.status in (self.IN_REVIEW, self.MERGE_ERROR)
