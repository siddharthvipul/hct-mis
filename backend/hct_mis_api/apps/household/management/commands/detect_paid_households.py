from django.core.management import BaseCommand
from django.db.models import Q

from hct_mis_api.apps.payment.models import PaymentRecord
from hct_mis_api.apps.household.models import Household
from hct_mis_api.apps.household.models import Document
from hct_mis_api.apps.core.models import StorageFile


def find_paid_households(sf_pk, business_area_slug="ukraine"):
    storage_file = StorageFile.objects.get(pk=sf_pk)
    households_loaded_via_sf = Household.objects.filter(storage_obj=storage_file)
    tax_ids_of_inds_loaded_via_sf = Document.objects.filter(
        individual__household__in=households_loaded_via_sf, type__type="TAX_ID"
    ).values_list("document_number", flat=True)
    hh_ids_not_loaded_via_sf = Household.objects.filter(
        Q(
            business_area__slug=business_area_slug,
            individuals__documents__document_number__in=tax_ids_of_inds_loaded_via_sf,
        )
        & ~Q(storage_obj=storage_file)
    ).values_list("id", flat=True)
    payment_records = PaymentRecord.objects.filter(household__id__in=hh_ids_not_loaded_via_sf).distinct("household")
    already_paid_households = payment_records.values_list("household", flat=True)

    def match(household_to_match):
        tax_ids_in_household_to_match = Document.objects.filter(
            individual__household=household_to_match, type__type="TAX_ID"
        ).values_list("document_number", flat=True)
        return Household.objects.filter(
            Q(
                business_area__slug=business_area_slug,
                individuals__documents__document_number__in=tax_ids_in_household_to_match,
                storage_obj=storage_file,
            )
        ).values_list("id", flat=True)

    return {hh: match(hh) for hh in already_paid_households}


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("storage_file_pk", type=int)

        parser.add_argument(
            "--business-area-slug",
            type=str,
            default="ukraine",
        )

    def handle(self, *args, **options):
        if not options["storage_file_pk"]:
            raise ValueError("storage_file_pk arg is required")

        if not options["business_area_slug"]:
            raise ValueError("business_area_slug arg is required")

        households = find_paid_households(options["storage_file_pk"], options["business_area_slug"])
        for household, matches in households.items():
            self.stdout.write(f"Household {household} has already been paid and matches {matches}")
