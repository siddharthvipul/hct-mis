import logging

from django import forms
from django.contrib import admin, messages
from django.contrib.admin import SimpleListFilter
from django.contrib.messages import ERROR
from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils.html import format_html

import xlrd
from admin_extra_urls.api import ExtraUrlMixin, button
from adminfilters.filters import ChoicesFieldComboFilter
from xlrd import XLRDError

from hct_mis_api.apps.core.celery_tasks import (
    upload_new_kobo_template_and_update_flex_fields_task,
)
from hct_mis_api.apps.core.datamart.api import DatamartAPI
from hct_mis_api.apps.core.models import (
    AdminArea,
    AdminAreaLevel,
    BusinessArea,
    CountryCodeMap,
    FlexibleAttribute,
    FlexibleAttributeChoice,
    FlexibleAttributeGroup,
    XLSXKoboTemplate,
)
from hct_mis_api.apps.core.validators import KoboTemplateValidator
from hct_mis_api.apps.payment.rapid_pro.api import RapidProAPI
from mptt.admin import MPTTModelAdmin

logger = logging.getLogger(__name__)


class XLSImportForm(forms.Form):
    xls_file = forms.FileField()


class TestRapidproForm(forms.Form):
    phone_number = forms.CharField(
        label="Phone number",
        required=True,
    )
    flow_name = forms.CharField(label="Name of the test flow", initial="Test", required=True)


@admin.register(BusinessArea)
class BusinessAreaAdmin(ExtraUrlMixin, admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "code",
        "region_name",
        "region_code",
    )
    search_fields = ("name", "slug")
    list_filter = ("has_data_sharing_agreement", "region_name")

    @button(label="Test RapidPro Connection")
    def _test_rapidpro_connection(self, request, pk):
        context = self.get_common_context(request, pk)
        context["business_area"] = self.object
        context["title"] = f"Test `{self.object.name}` RapidPRO connection"

        api = RapidProAPI(self.object.slug)

        if request.method == "GET":
            phone_number = request.GET.get("phone_number", None)
            flow_uuid = request.GET.get("flow_uuid", None)
            flow_name = request.GET.get("flow_name", None)
            timestamp = request.GET.get("timestamp", None)

            if all([phone_number, flow_uuid, flow_name, timestamp]):
                error, result = api.test_connection_flow_run(flow_uuid, phone_number, timestamp)
                context["run_result"] = result
                context["phone_number"] = phone_number
                context["flow_uuid"] = flow_uuid
                context["flow_name"] = flow_name
                context["timestamp"] = timestamp

                if error:
                    messages.error(request, error)
                else:
                    messages.success(request, "Connection successful")
            else:
                context["form"] = TestRapidproForm()
        else:
            form = TestRapidproForm(request.POST)
            if form.is_valid():
                phone_number = form.cleaned_data["phone_number"]
                flow_name = form.cleaned_data["flow_name"]
                context["phone_number"] = phone_number
                context["flow_name"] = flow_name

                error, response = api.test_connection_start_flow(flow_name, phone_number)
                if response:
                    context["flow_uuid"] = response["flow"]["uuid"]
                    context["flow_status"] = response["status"]
                    context["timestamp"] = response["created_on"]

                if error:
                    messages.error(request, error)
                else:
                    messages.success(request, "Connection successful")

            context["form"] = form

        return TemplateResponse(request, "core/test_rapidpro.html", context)


class AdminLevelFilter(SimpleListFilter):
    template = "adminfilters/combobox.html"

    title = "Admin Level"
    parameter_name = "alevel"

    def lookups(self, request, model_admin):
        return [(l, f"Level {l}") for l in range(3)]

    def value(self):
        return self.used_parameters.get(self.parameter_name)

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(admin_area_level__admin_level=self.value())
        return queryset


class LoadAdminAreaForm(forms.Form):
    area = forms.ModelChoiceField(BusinessArea.objects.all())


@admin.register(AdminArea)
class AdminAreaAdmin(ExtraUrlMixin, admin.ModelAdmin):
    search_fields = (
        "p_code",
        "title",
    )
    list_display = ("title", "parent", "admin_area_level", "p_code")
    list_filter = (AdminLevelFilter,)

    @button()
    def load_from_datamart(self, request):
        #         business_area = BusinessArea.objects.filter(name=options["business_area"][0]).first()
        #         api = DatamartAPI()
        #         locations = api.get_locations_geo_data(business_area)
        #         admin_areas = api.generate_admin_areas(locations, business_area)
        context = self.get_common_context(request)
        if request.method == "GET":
            form = LoadAdminAreaForm()
            context["form"] = form
        else:
            form = LoadAdminAreaForm(data=request.POST)
            if form.is_valid():
                try:
                    business_area = form.cleaned_data["area"]
                    api = DatamartAPI()
                    locations = api.get_locations_geo_data(business_area)
                    admin_areas = api.generate_admin_areas(locations, business_area)
                    context["admin_areas"] = admin_areas
                except Exception as e:
                    context["form"] = form
                    self.message_user(request, str(e), messages.ERROR)

        return TemplateResponse(request, "core/admin/load_admin_areas.html", context)


@admin.register(AdminAreaLevel)
class AdminAreaLevelAdmin(admin.ModelAdmin):
    list_display = ("name", "business_area")


class FlexibleAttributeInline(admin.TabularInline):
    model = FlexibleAttribute
    fields = readonly_fields = ("name", "associated_with", "required")
    extra = 0


@admin.register(FlexibleAttribute)
class FlexibleAttributeAdmin(admin.ModelAdmin):
    list_display = ("type", "name", "required")
    list_filter = (
        ("type", ChoicesFieldComboFilter),
        ("associated_with", ChoicesFieldComboFilter),
        "required",
        "is_removed",
    )
    search_fields = ("name",)


@admin.register(FlexibleAttributeGroup)
class FlexibleAttributeGroupAdmin(MPTTModelAdmin):
    inlines = (FlexibleAttributeInline,)
    list_display = ("name", "parent", "required", "repeatable", "is_removed")
    autocomplete_fields = ("parent",)
    list_filter = ("repeatable", "required", "is_removed")
    search_fields = ("name",)


@admin.register(FlexibleAttributeChoice)
class FlexibleAttributeChoiceAdmin(admin.ModelAdmin):
    list_display = (
        "list_name",
        "name",
    )
    search_fields = ("name", "list_name")
    list_filter = ("is_removed",)
    filter_horizontal = ("flex_attributes",)


@admin.register(XLSXKoboTemplate)
class XLSXKoboTemplateAdmin(ExtraUrlMixin, admin.ModelAdmin):
    list_display = ("original_file_name", "uploaded_by", "created_at", "file", "import_status")

    exclude = ("is_removed", "file_name", "status", "template_id")

    readonly_fields = ("original_file_name", "uploaded_by", "file", "import_status", "error_description")

    def import_status(self, obj):
        if obj.status == self.model.SUCCESSFUL:
            color = "89eb34"
        elif obj.status == self.model.UNSUCCESSFUL:
            color = "e30b0b"
        else:
            color = "7a807b"

        return format_html(
            '<span style="color: #{};">{}</span>',
            color,
            obj.status,
        )

    def original_file_name(self, obj):
        return obj.file_name

    def get_form(self, request, obj=None, change=False, **kwargs):
        if obj is None:
            return XLSImportForm
        return super().get_form(request, obj, change, **kwargs)

    @button()
    def download_last_valid_file(self, request):
        latest_valid_import = self.model.objects.latest_valid()
        if latest_valid_import:
            return redirect(latest_valid_import.file.url)
        self.message_user(
            request,
            "There is no valid file to download",
            level=ERROR,
        )

    @button(label="Rerun KOBO Import", visible=lambda o: o is not None and o.status != XLSXKoboTemplate.SUCCESSFUL)
    def rerun_kobo_import(self, request, pk):
        xlsx_kobo_template_object = get_object_or_404(XLSXKoboTemplate, pk=pk)
        upload_new_kobo_template_and_update_flex_fields_task.run(
            xlsx_kobo_template_id=str(xlsx_kobo_template_object.id)
        )
        return redirect(".")

    def add_view(self, request, form_url="", extra_context=None):
        if not self.has_add_permission(request):
            logger.error("The user did not have permission to do that")
            raise PermissionDenied

        opts = self.model._meta
        app_label = opts.app_label

        context = {
            **self.admin_site.each_context(request),
            "opts": opts,
            "app_label": app_label,
            "has_file_field": True,
        }
        form_class = self.get_form(request)
        payload = {**context}

        if request.method == "POST":
            form = form_class(request.POST, request.FILES)
            payload["form"] = form
            xls_file = request.FILES["xls_file"]

            try:
                wb = xlrd.open_workbook(file_contents=xls_file.read())
                sheets = {
                    "survey_sheet": wb.sheet_by_name("survey"),
                    "choices_sheet": wb.sheet_by_name("choices"),
                }
                validation_errors = KoboTemplateValidator.validate_kobo_template(**sheets)
                if validation_errors:
                    errors = [f"Field: {error['field']} - {error['message']}" for error in validation_errors]
                    form.add_error(field=None, error=errors)
            except ValidationError as validation_error:
                logger.exception(validation_error)
                form.add_error("xls_file", validation_error)
            except XLRDError as file_error:
                logger.exception(file_error)
                form.add_error("xls_file", file_error)

            if form.is_valid():
                xlsx_kobo_template_object = XLSXKoboTemplate.objects.create(
                    file_name=xls_file.name,
                    uploaded_by=request.user,
                    file=xls_file,
                    status=XLSXKoboTemplate.UPLOADED,
                )
                self.message_user(
                    request,
                    "Core field validation successful, running KoBo Template upload task..., "
                    "Import status will change after task completion",
                )
                upload_new_kobo_template_and_update_flex_fields_task.run(
                    xlsx_kobo_template_id=str(xlsx_kobo_template_object.id)
                )
                return redirect("..")
        else:
            payload["form"] = form_class()

        return TemplateResponse(request, "core/xls_form.html", payload)

    def change_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = dict(show_save=False, show_save_and_continue=False, show_delete=True)
        has_add_permission = self.has_add_permission
        self.has_add_permission = lambda __: False
        template_response = super().change_view(request, object_id, form_url, extra_context)
        self.has_add_permission = has_add_permission

        return template_response


@admin.register(CountryCodeMap)
class CountryCodeMapAdmin(ExtraUrlMixin, admin.ModelAdmin):
    list_display = ("country", "alpha2", "alpha3", "ca_code")
    search_fields = ("country",)

    def alpha2(self, obj):
        return obj.country.countries.alpha2(obj.country.code)

    def alpha3(self, obj):
        return obj.country.countries.alpha3(obj.country.code)
