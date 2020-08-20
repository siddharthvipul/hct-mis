from django.db import models
from django.utils.translation import ugettext_lazy as _

from household.models import (
    RELATIONSHIP_CHOICE,
    ROLE_CHOICE,
    MARITAL_STATUS_CHOICE,
    INDIVIDUAL_HOUSEHOLD_STATUS,
    RESIDENCE_STATUS_CHOICE,
    IDENTIFICATION_TYPE_CHOICE,
)
from utils.models import AbstractSession


class Session(AbstractSession):
    pass


class SessionModel(models.Model):
    session = models.ForeignKey("Session", on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Household(SessionModel):
    mis_id = models.UUIDField()
    unhcr_id = models.CharField(max_length=255, null=True)
    unicef_id = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=20, choices=INDIVIDUAL_HOUSEHOLD_STATUS, default="ACTIVE")
    household_size = models.PositiveIntegerField()
    # registration household id
    form_number = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    admin1 = models.CharField(max_length=255, null=True)
    admin2 = models.CharField(max_length=255, null=True)
    country = models.CharField(null=True, max_length=3)
    residence_status = models.CharField(max_length=255, choices=RESIDENCE_STATUS_CHOICE, null=True)
    registration_date = models.DateField(null=True)

    class Meta:
        unique_together = ("session", "mis_id")


class Individual(SessionModel):
    INACTIVE = "INACTIVE"
    ACTIVE = "ACTIVE"
    STATUS_CHOICE = ((INACTIVE, "Inactive"), (ACTIVE, "Active"))
    MALE = "MALE"
    FEMALE = "FEMALE"
    SEX_CHOICE = (
        (MALE, _("Male")),
        (FEMALE, _("Female")),
    )

    mis_id = models.UUIDField()
    unhcr_id = models.CharField(max_length=255, null=True)
    unicef_id = models.CharField(max_length=255, null=True)
    household_mis_id = models.UUIDField(null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICE, null=True,)
    national_id_number = models.CharField(max_length=255, null=True)
    full_name = models.CharField(max_length=255)
    family_name = models.CharField(max_length=255, null=True)
    given_name = models.CharField(max_length=255, null=True)
    middle_name = models.CharField(max_length=255, null=True)
    sex = models.CharField(max_length=255, choices=SEX_CHOICE,)
    date_of_birth = models.DateField()
    estimated_date_of_birth = models.BooleanField()
    relationship = models.CharField(max_length=255, null=True, choices=RELATIONSHIP_CHOICE,)
    marital_status = models.CharField(max_length=255, choices=MARITAL_STATUS_CHOICE,)
    phone_number = models.CharField(max_length=14, null=True)

    class Meta:
        unique_together = ("session", "mis_id")

    def __str__(self):
        return self.family_name


class TargetPopulation(SessionModel):
    mis_id = models.UUIDField()
    name = models.CharField(max_length=255)
    population_type = models.CharField(default="HOUSEHOLD", max_length=20)
    targeting_criteria = models.TextField()

    active_households = models.PositiveIntegerField(default=0)
    program_mis_id = models.UUIDField()

    class Meta:
        unique_together = ("session", "mis_id")

    def __str__(self):
        return self.name


class IndividualRoleInHousehold(SessionModel):
    individual_mis_id = models.UUIDField()
    household_mis_id = models.UUIDField()
    role = models.CharField(max_length=255, blank=True, choices=ROLE_CHOICE,)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("role", "household_mis_id", "session")


class TargetPopulationEntry(SessionModel):
    household_unhcr_id = models.CharField(max_length=255, null=True)
    individual_unhcr_id = models.CharField(max_length=255, null=True)
    household_mis_id = models.UUIDField(null=True)
    individual_mis_id = models.UUIDField(null=True)
    target_population_mis_id = models.UUIDField()
    vulnerability_score = models.DecimalField(
        blank=True, null=True, decimal_places=3, max_digits=6, help_text="Written by a tool such as Corticon.",
    )

    class Meta:
        unique_together = (
            "session",
            "household_mis_id",
            "target_population_mis_id",
        )


class Program(SessionModel):
    STATUS_NOT_STARTED = "NOT_STARTED"
    STATUS_STARTED = "STARTED"
    STATUS_COMPLETE = "COMPLETE"
    SCOPE_FOR_PARTNERS = "FOR_PARTNERS"
    SCOPE_UNICEF = "UNICEF"
    SCOPE_CHOICE = (
        (SCOPE_FOR_PARTNERS, _("For partners")),
        (SCOPE_UNICEF, _("Unicef")),
    )
    mis_id = models.UUIDField()
    business_area = models.CharField(max_length=20)
    ca_id = models.CharField(max_length=255)
    ca_hash_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    scope = models.CharField(choices=SCOPE_CHOICE, max_length=50)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.CharField(max_length=255, null=True)
    individual_data_needed = models.BooleanField(default=False)

    class Meta:
        unique_together = ("session", "mis_id")


class Document(SessionModel):
    VALID = "VALID"
    COLLECTED = "COLLECTED"
    LOST = "LOST"
    UNKNOWN = "UNKNOWN"
    CANCELED = "CANCELED"
    EXPIRED = "EXPIRED"
    HOLD = "HOLD"
    DAMAGED = "DAMAGED"
    STATUS_CHOICE = (
        (VALID, _("Valid")),
        (COLLECTED, _("Collected")),
        (LOST, _("Lost")),
        (UNKNOWN, _("Unknown")),
        (CANCELED, _("Canceled")),
        (EXPIRED, _("Expired")),
        (HOLD, _("Hold")),
        (DAMAGED, _("Damaged")),
    )

    status = models.CharField(choices=STATUS_CHOICE, null=True, max_length=30, default=None)
    date_of_expiry = models.DateField(null=True, default=None)
    photo = models.ImageField(blank=True, default="")
    mis_id = models.UUIDField()
    number = models.CharField(max_length=255, null=True)
    individual_mis_id = models.UUIDField(null=True)
    type = models.CharField(max_length=50, choices=IDENTIFICATION_TYPE_CHOICE)
