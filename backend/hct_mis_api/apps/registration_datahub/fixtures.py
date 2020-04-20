import factory.fuzzy
from pytz import utc

from household.const import NATIONALITIES
from household.models import (
    RESIDENCE_STATUS_CHOICE,
    SEX_CHOICE,
    YES_NO_CHOICE,
    MARTIAL_STATUS_CHOICE,
    IDENTIFICATION_TYPE_CHOICE,
)
from registration_datahub.models import (
    RegistrationDataImportDatahub,
    ImportedHousehold,
    ImportedIndividual,
)


class RegistrationDataImportDatahubFactory(factory.DjangoModelFactory):
    class Meta:
        model = RegistrationDataImportDatahub

    name = factory.Faker(
        "sentence", nb_words=6, variable_nb_words=True, ext_word_list=None,
    )
    import_date = factory.Faker(
        "date_time_this_decade", before_now=True, tzinfo=utc,
    )


class ImportedHouseholdFactory(factory.DjangoModelFactory):
    class Meta:
        model = ImportedHousehold

    household_ca_id = factory.Faker("uuid4")
    consent = factory.django.ImageField(color="blue")
    residence_status = factory.fuzzy.FuzzyChoice(
        RESIDENCE_STATUS_CHOICE, getter=lambda c: c[0],
    )
    country_origin = factory.fuzzy.FuzzyChoice(
        NATIONALITIES, getter=lambda c: c[0],
    )
    size = factory.fuzzy.FuzzyInteger(3, 8)
    address = factory.Faker("address")
    registration_data_import = factory.SubFactory(
        RegistrationDataImportDatahubFactory,
    )
    registration_date = factory.Faker(
        "date_this_year", before_today=True, after_today=False
    )


class ImportedIndividualFactory(factory.DjangoModelFactory):
    class Meta:
        model = ImportedIndividual

    individual_ca_id = factory.Faker("uuid4")
    full_name = factory.LazyAttribute(
        lambda o: f"{o.given_name} {o.middle_name} {o.family_name}"
    )
    given_name = factory.Faker("first_name")
    middle_name = factory.Faker("first_name")
    family_name = factory.Faker("last_name")
    sex = factory.fuzzy.FuzzyChoice(SEX_CHOICE, getter=lambda c: c[0],)
    birth_date = factory.Faker(
        "date_of_birth", tzinfo=utc, minimum_age=16, maximum_age=90
    )
    estimated_dob = factory.fuzzy.FuzzyChoice(
        YES_NO_CHOICE, getter=lambda c: c[0],
    )

    martial_status = factory.fuzzy.FuzzyChoice(
        MARTIAL_STATUS_CHOICE, getter=lambda c: c[0],
    )
    phone_number = factory.Faker("phone_number")
    phone_number_alternative = ""
    identification_type = factory.fuzzy.FuzzyChoice(
        IDENTIFICATION_TYPE_CHOICE, getter=lambda c: c[0],
    )
    birth_certificate_no = ""
    birth_certificate_photo = ""
    drivers_license_no = ""
    drivers_license_photo = ""
    electoral_card_no = ""
    electoral_card_photo = ""
    unhcr_id_no = ""
    unhcr_id_photo = ""
    national_passport = ""
    national_passport_photo = ""
    scope_id_no = ""
    scope_id_photo = ""
    other_id_type = ""
    other_id_no = ""
    other_id_photo = ""
    registration_data_import = factory.SubFactory(
        RegistrationDataImportDatahubFactory
    )
    work_status = factory.fuzzy.FuzzyChoice(
        YES_NO_CHOICE, getter=lambda c: c[0],
    )
    disability = factory.fuzzy.FuzzyChoice(
        YES_NO_CHOICE, getter=lambda c: c[0],
    )
    household = factory.SubFactory(ImportedHouseholdFactory)
