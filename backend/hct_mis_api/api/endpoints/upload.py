import base64

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile
from django.db.transaction import atomic
from django.utils import timezone
from django.utils.functional import cached_property

from django_countries import Countries
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from hct_mis_api.api.endpoints.base import HOPEAPIView, SelectedBusinessAreaMixin
from hct_mis_api.apps.account.permissions import Permissions
from hct_mis_api.apps.core.models import BusinessArea
from hct_mis_api.apps.household.models import (
    HEAD,
    IDENTIFICATION_TYPE_CHOICE,
    NON_BENEFICIARY,
    RELATIONSHIP_UNKNOWN,
    ROLE_ALTERNATE,
    ROLE_NO_ROLE,
    ROLE_PRIMARY,
)
from hct_mis_api.apps.registration_datahub.models import (
    ImportedDocument,
    ImportedDocumentType,
)
from hct_mis_api.apps.registration_datahub.models import ImportedHousehold as Household
from hct_mis_api.apps.registration_datahub.models import (
    ImportedIndividual as Individual,
)
from hct_mis_api.apps.registration_datahub.models import RegistrationDataImportDatahub

DETAILS_POLICY = (
    ["NO", "NO"],
    ["FULL", "FULL"],
    ["PARTIAL", "PARTIAL"],
)


class MemberSerializer(serializers.ListSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.head_of_household = None
        self.alternate_collector = None
        self.primary_collector = None

    def validate(self, attrs):
        for data in attrs:
            if data["relationship"] == HEAD:
                if self.head_of_household:
                    ValidationError("Invalid head_of_households number ")
                self.head_of_household = data
            if data["role"] == ROLE_PRIMARY:
                if self.head_of_household:
                    ValidationError("Invalid primary_collector number ")
                self.primary_collector = data
            if data["role"] == ROLE_ALTERNATE:
                if self.head_of_household:
                    ValidationError("Invalid alternate_collector number ")
                self.alternate_collector = data
        return attrs


class DocumentSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices=IDENTIFICATION_TYPE_CHOICE, allow_blank=True, required=False)
    country = serializers.ChoiceField(choices=Countries())
    image = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = ImportedDocument
        exclude = [
            "individual",
            "photo",
        ]


class IndividualSerializer(serializers.ModelSerializer):
    first_registration_date = serializers.DateTimeField(default=timezone.now)
    last_registration_date = serializers.DateTimeField(default=timezone.now)
    unicef_id = serializers.ReadOnlyField()
    household = serializers.ReadOnlyField()
    role = serializers.CharField(allow_blank=True)
    observed_disability = serializers.CharField(allow_blank=True, required=False)
    country_origin = serializers.CharField(allow_blank=True, required=False)
    marital_status = serializers.CharField(allow_blank=True, required=False)
    documents = DocumentSerializer(many=True, required=False)

    class Meta:
        model = Individual
        exclude = ["id", "registration_data_import"]
        list_serializer_class = MemberSerializer

    def validate_role(self, value):
        if value in [ROLE_NO_ROLE, ROLE_PRIMARY, ROLE_ALTERNATE]:
            return value
        if not value:
            return ROLE_NO_ROLE
        elif value.upper()[0] == "P":
            return ROLE_PRIMARY
        elif value.upper()[0] == "A":
            return ROLE_ALTERNATE
        raise ValidationError(f"Invalid role '{value}'")

    def save(self, **kwargs):
        self.validated_data.pop("role")
        return super().save(**kwargs)

    def validate(self, attrs):
        self.documents = DocumentSerializer(data=attrs.get("documents", []), many=True)
        self.documents.is_valid(True)
        return super().validate(attrs)

    @atomic()
    def create(self, validated_data):
        self.documents = validated_data.pop("documents", [])
        return super().create(validated_data)


def get_photo_from_stream(stream):
    if stream:
        base64_img_bytes = stream.encode("utf-8")
        decoded_image_data = base64.decodebytes(base64_img_bytes)
        return SimpleUploadedFile("photo.png", decoded_image_data, content_type="image/png")

    return None


class HouseholdSerializer(serializers.ModelSerializer):
    unicef_id = serializers.ReadOnlyField()
    first_registration_date = serializers.DateTimeField(default=timezone.now)
    last_registration_date = serializers.DateTimeField(default=timezone.now)
    collect_individual_data = serializers.CharField()
    members = IndividualSerializer(many=True)
    country_origin = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Household
        exclude = ["id", "head_of_household", "registration_data_import"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.members = None

    def validate(self, attrs):
        self.members = IndividualSerializer(data=attrs["members"], many=True)
        self.members.is_valid(True)
        return super().validate(attrs)

    def save(self, **kwargs):
        self.validated_data.pop("members")
        return super().save(**kwargs)


class RDISerializer(serializers.ModelSerializer):
    households = HouseholdSerializer(many=True)

    class Meta:
        model = RegistrationDataImportDatahub
        exclude = ("business_area_slug", "import_data")

    def __init__(self, *args, **kwargs):
        self.business_area = kwargs.pop("business_area")
        super().__init__(*args, **kwargs)

    @atomic()
    def create(self, validated_data):
        households = validated_data.pop("households")
        rdi = RegistrationDataImportDatahub.objects.create(**validated_data, business_area_slug=self.business_area.slug)
        try:
            for i, household_data in enumerate(households):
                hh_ser = HouseholdSerializer(data=household_data)
                if hh_ser.is_valid():
                    members: MemberSerializer = hh_ser.members
                    hoh_ser = IndividualSerializer(data=members.head_of_household)
                    if hoh_ser.is_valid(True):
                        hh: Household = hh_ser.save(head_of_household=None, registration_data_import=rdi)
                        primary = None
                        alternate = None
                        for member_data in members.validated_data:
                            member_ser = IndividualSerializer(data=member_data)
                            if member_ser.is_valid():
                                if member_data["relationship"] in [RELATIONSHIP_UNKNOWN, NON_BENEFICIARY]:
                                    member_of = None
                                else:
                                    member_of = hh
                                member = member_ser.save(household=member_of, registration_data_import=rdi)
                                for doc in member_ser.documents:
                                    ImportedDocument.objects.create(
                                        document_number=doc["document_number"],
                                        photo=get_photo_from_stream(doc["image"]),
                                        doc_date=doc["doc_date"],
                                        individual=member,
                                        type=ImportedDocumentType.objects.get(country=doc["country"], type=doc["type"]),
                                    )
                                if member_data["relationship"] == HEAD:
                                    assert member.household == hh
                                    hh.head_of_household = member
                                    hh.save()
                                if member_data["role"] == ROLE_PRIMARY:
                                    primary = member
                                elif member_data["role"] == ROLE_ALTERNATE:
                                    alternate = member
                        hh.individuals_and_roles.create(individual=primary, role=ROLE_PRIMARY)
                        if alternate:
                            hh.individuals_and_roles.create(individual=primary, role=ROLE_ALTERNATE)
                else:
                    raise ValidationError(hh_ser.errors, code=f"Error validating Household in position #{i}")
        except Exception as e:
            logger.exception(e)
            raise
        return rdi


class UploadRDIView(SelectedBusinessAreaMixin, HOPEAPIView):
    permission = Permissions.API_UPLOAD_RDI

    def post(self, request, business_area):
        serializer = RDISerializer(data=request.data, business_area=self.selected_business_area)
        if serializer.is_valid():
            serializer.save()
            return Response({}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
