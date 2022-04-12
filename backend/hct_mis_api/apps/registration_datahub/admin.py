import base64
import datetime
import json
import logging

import requests
from admin_extra_buttons.decorators import button, link
from admin_extra_buttons.mixins import ExtraButtonsMixin
from adminactions.mass_update import mass_update
from adminfilters.autocomplete import AutoCompleteFilter
from adminfilters.depot.widget import DepotManager
from adminfilters.filters import ChoicesFieldComboFilter, NumberFilter, ValueFilter
from adminfilters.querystring import QueryStringFilter
from advanced_filters.admin import AdminAdvancedFiltersMixin
from django import forms
from django.contrib import admin, messages
from django.core.signing import BadSignature, Signer
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.safestring import mark_safe
from requests.auth import HTTPBasicAuth

from hct_mis_api.apps.registration_datahub.celery_tasks import process_flex_records_task
from hct_mis_api.apps.registration_datahub.models import (
    ImportData,
    ImportedDocument,
    ImportedDocumentType,
    ImportedHousehold,
    ImportedIndividual,
    ImportedIndividualIdentity,
    ImportedIndividualRoleInHousehold,
    KoboImportedSubmission,
    Record,
    RegistrationDataImportDatahub,
)
from hct_mis_api.apps.registration_datahub.services.flex_registration_service import FlexRegistrationService
from hct_mis_api.apps.registration_datahub.utils import post_process_dedupe_results
from hct_mis_api.apps.utils.admin import HOPEModelAdminBase
from hct_mis_api.apps.utils.security import is_root

logger = logging.getLogger(__name__)


@admin.register(RegistrationDataImportDatahub)
class RegistrationDataImportDatahubAdmin(ExtraButtonsMixin, AdminAdvancedFiltersMixin, HOPEModelAdminBase):
    list_display = ("name", "import_date", "import_done", "business_area_slug", "hct_id")
    list_filter = ("created_at", "import_done", ("business_area_slug", ValueFilter.factory(lookup_name="istartswith")))
    advanced_filter_fields = (
        "created_at",
        "import_done",
        ("business_area__name", "business area"),
    )

    raw_id_fields = ("import_data",)
    date_hierarchy = "created_at"
    search_fields = ("name",)

    @link(
        href=None,
        label="RDI",
    )
    def hub(self, button):
        obj = button.context.get("original")
        if obj:
            if obj.hct_id:
                return reverse("admin:registration_data_registrationdataimport_change", args=[obj.hct_id])
            else:
                button.html_attrs = {"style": "background-color:#CCCCCC;cursor:not-allowed"}
                return "javascript:alert('RDI not imported');"
        button.visible = False

    @button()
    def inspect(self, request, pk):
        context = self.get_common_context(request, pk)
        obj: RegistrationDataImportDatahub = context["original"]
        context["title"] = f"Import {obj.name} - {obj.import_done}"
        context["data"] = {}
        has_content = False
        for model in [ImportedIndividual, ImportedHousehold]:
            count = model.objects.filter(registration_data_import=obj).count()
            has_content = has_content or count
            context["data"][model] = {"count": count, "warnings": [], "errors": [], "meta": model._meta}

        return TemplateResponse(request, "registration_datahub/admin/inspect.html", context)


@admin.register(ImportedIndividual)
class ImportedIndividualAdmin(ExtraButtonsMixin, HOPEModelAdminBase):
    list_display = (
        "registration_data_import",
        "individual_id",
        "full_name",
        "sex",
        "dedupe_status",
        "score",
        "batch_score",
    )
    list_filter = (
        ("deduplication_batch_results", NumberFilter),
        ("deduplication_golden_record_results", NumberFilter),
        ("registration_data_import__name", ValueFilter.factory(lookup_name="istartswith")),
        ("individual_id", ValueFilter.factory(lookup_name="istartswith")),
        "deduplication_batch_status",
        "deduplication_golden_record_status",
    )
    date_hierarchy = "updated_at"
    # raw_id_fields = ("household", "registration_data_import")
    autocomplete_fields = ("household", "registration_data_import")
    actions = ["enrich_deduplication"]

    def score(self, obj):
        try:
            return obj.deduplication_golden_record_results["score"]["max"]
        except KeyError:
            return ""

    def batch_score(self, obj):
        try:
            return obj.deduplication_batch_results["score"]["max"]
        except KeyError:
            return ""

    def dedupe_status(self, obj):
        lbl = f"{obj.deduplication_batch_status}/{obj.deduplication_golden_record_status}"
        url = reverse("admin:registration_datahub_importedindividual_duplicates", args=[obj.pk])
        if "duplicates" in obj.deduplication_batch_results:
            ret = f'<a href="{url}">{lbl}</a>'
        elif "duplicates" in obj.deduplication_golden_record_results:
            ret = f'<a href="{url}">{lbl}</a>'
        else:
            ret = lbl
        return mark_safe(ret)

    def enrich_deduplication(self, request, queryset):
        for record in queryset.exclude(deduplication_batch_results__has_key="score"):
            post_process_dedupe_results(record)

    @button()
    def post_process_dedupe_results(self, request, pk):
        record = self.get_queryset(request).get(id=pk)
        post_process_dedupe_results(record)
        record.save()

    @button()
    def duplicates(self, request, pk):
        ctx = self.get_common_context(request, pk, title="Duplicates")
        return TemplateResponse(request, "registration_datahub/admin/duplicates.html", ctx)


@admin.register(ImportedIndividualIdentity)
class ImportedIndividualIdentityAdmin(HOPEModelAdminBase):
    raw_id_fields = ("individual",)


@admin.register(ImportedHousehold)
class ImportedHouseholdAdmin(HOPEModelAdminBase):
    search_fields = ("id", "registration_data_import")
    list_display = ("registration_data_import", "registration_method", "name_enumerator", "country", "country_origin")
    raw_id_fields = ("registration_data_import", "head_of_household")
    date_hierarchy = "registration_data_import__import_date"
    list_filter = (
        ("country", ChoicesFieldComboFilter),
        ("country_origin", ChoicesFieldComboFilter),
        ("registration_data_import__name", ValueFilter.factory(lookup_name="istartswith")),
        ("kobo_submission_uuid", ValueFilter.factory(lookup_name="istartswith")),
        ("kobo_submission_uuid", ValueFilter.factory(lookup_name="istartswith")),
    )


@admin.register(ImportData)
class ImportDataAdmin(HOPEModelAdminBase):
    list_filter = ("data_type",)
    date_hierarchy = "created_at"


@admin.register(ImportedDocumentType)
class ImportedDocumentTypeAdmin(HOPEModelAdminBase):
    list_display = ("label", "country")
    list_filter = (("country", ChoicesFieldComboFilter),)


@admin.register(ImportedDocument)
class ImportedDocumentAdmin(HOPEModelAdminBase):
    list_display = ("document_number", "type", "individual")
    raw_id_fields = ("individual", "type")
    list_filter = (("type", AutoCompleteFilter),)


@admin.register(ImportedIndividualRoleInHousehold)
class ImportedIndividualRoleInHouseholdAdmin(HOPEModelAdminBase):
    raw_id_fields = ("individual", "household")
    list_filter = ("role",)


@admin.register(KoboImportedSubmission)
class KoboImportedSubmissionAdmin(AdminAdvancedFiltersMixin, HOPEModelAdminBase):
    list_display = (
        "created_at",
        "kobo_submission_time",
        "kobo_submission_uuid",
        "kobo_asset_id",
        "amended",
        "imported_household_id",
        "registration_data_import_id",
    )
    # date_hierarchy = "created_at"
    list_filter = (
        "amended",
        ("registration_data_import", AutoCompleteFilter),
        ("imported_household", AutoCompleteFilter),
    )
    advanced_filter_fields = (
        # "created_at",
        "amended",
        "kobo_submission_time",
        "registration_data_import_id",
    )
    raw_id_fields = ("registration_data_import", "imported_household")


class FetchForm(forms.Form):
    SYNC_COOKIE = "fetch"

    host = forms.URLField()
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    registration = forms.IntegerField()
    start = forms.IntegerField()
    end = forms.IntegerField()
    remember = forms.BooleanField(label="Remember me", required=False)

    def get_signed_cookie(self, request):
        signer = Signer(request.user.password)
        return signer.sign_object(self.cleaned_data)

    @classmethod
    def get_saved_config(cls, request):
        try:
            signer = Signer(request.user.password)
            obj: dict = signer.unsign_object(request.COOKIES.get(cls.SYNC_COOKIE, {}))
            return obj
        except BadSignature:
            return {}


@admin.register(Record)
class RecordDatahubAdmin(ExtraButtonsMixin, HOPEModelAdminBase):
    list_display = ("id", "registration", "timestamp", "source_id", "ignored")
    readonly_fields = ("id", "registration", "timestamp", "source_id", "ignored")
    exclude = ("data",)
    date_hierarchy = "timestamp"
    list_filter = (
        DepotManager,
        ("source_id", NumberFilter),
        ("id", NumberFilter),
        "timestamp",
        QueryStringFilter,
    )
    change_form_template = "registration_datahub/admin/record/change_form.html"
    change_list_template = "registration_datahub/admin/record/change_list.html"

    actions = [mass_update, "extract", "create_rdi"]
    mass_update_fields = [
        "fields",
    ]
    mass_update_hints = []

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.defer("storage", "data")
        return qs

    @admin.action(description="Create RDI")
    def create_rdi(self, request, queryset):
        service = FlexRegistrationService()
        try:
            rdi = service.create_rdi(request.user, f"ukraine rdi {datetime.datetime.now()}")

            records_ids = Record.objects.filter(id__in=queryset.values_list("id", flat=True))
            process_flex_records_task.delay(rdi.id, records_ids)
            self.message_user(request, f"RDI Import with name: {rdi.name} started", messages.SUCCESS)
        except Exception as e:
            self.message_user(request, str(e), messages.ERROR)
            print(e)

    def extract(self, request, queryset):
        def _filter(d):
            if isinstance(d, list):
                return [_filter(v) for v in d]
            elif isinstance(d, dict):
                return {k: _filter(v) for k, v in d.items()}
            else:
                return d

        for r in queryset.all():
            try:
                extracted = json.loads(r.storage.tobytes().decode())
                r.data = _filter(extracted)
                r.save()
            except Exception as e:
                logger.exception(e)

    @button(permission=is_root)
    def fetch(self, request):
        ctx = self.get_common_context(request)
        cookies = {}
        if request.method == "POST":
            form = FetchForm(request.POST)
            if form.is_valid():
                if form.cleaned_data["remember"]:
                    cookies = {form.SYNC_COOKIE: form.get_signed_cookie(request)}

                auth = HTTPBasicAuth(form.cleaned_data["username"], form.cleaned_data["password"])
                url = "{host}api/data/{registration}/{start}/{end}/".format(**form.cleaned_data)
                with requests.get(url, stream=True, auth=auth) as res:
                    if res.status_code != 200:
                        raise Exception(str(res))
                    payload = res.json()
                    for record in payload["data"]:
                        Record.objects.update_or_create(
                            source_id=record["id"],
                            registration=2,
                            defaults={"timestamp": record["timestamp"], "storage": base64.b64decode(record["storage"])},
                        )
        else:
            form = FetchForm(initial=FetchForm.get_saved_config(request))

        ctx["form"] = form
        response = TemplateResponse(request, "registration_datahub/admin/record/fetch.html", ctx)
        if cookies:
            for k, v in cookies.items():
                response.set_cookie(k, v)
        return response

    @button()
    def extract_all(self, request):
        self.extract(request, Record.objects.filter(data__isnull=True))

    @button(label="Extract")
    def extract_single(self, request, pk):
        self.extract(request, Record.objects.filter(pk=pk))

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# @admin.register(ImportedBankAccountInfo)
# class RecordDatahubAdmin(ExtraButtonsMixin, HOPEModelAdminBase):
#     pass
