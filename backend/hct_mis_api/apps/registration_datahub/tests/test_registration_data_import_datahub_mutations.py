import io
from typing import Any, List

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile

from parameterized import parameterized
from PIL import Image

from hct_mis_api.apps.account.fixtures import PartnerFactory, UserFactory
from hct_mis_api.apps.account.permissions import Permissions
from hct_mis_api.apps.core.base_test_case import APITestCase
from hct_mis_api.apps.core.fixtures import create_afghanistan
from hct_mis_api.apps.core.models import BusinessArea
from hct_mis_api.apps.program.fixtures import ProgramFactory
from hct_mis_api.apps.program.models import Program
from hct_mis_api.apps.registration_data.models import ImportData


class TestRegistrationDataImportDatahubMutations(APITestCase):
    databases = "__all__"

    UPLOAD_REGISTRATION_DATA_IMPORT_DATAHUB = """
    mutation UploadImportDataXLSXFile(
      $file: Upload!, $businessAreaSlug: String!
    ) {
      uploadImportDataXlsxFileAsync(
        file: $file, businessAreaSlug: $businessAreaSlug
      ) {
        importData {
          numberOfHouseholds
          numberOfIndividuals
          xlsxValidationErrors {
            rowNumber
            header
            message
            }
        }
        errors {
          rowNumber
          header
          message
        }
      }
    }
    """

    CREATE_REGISTRATION_DATA_IMPORT = """
    mutation RegistrationXlsxImportMutation(
      $registrationDataImportData: RegistrationXlsxImportMutationInput!
    ) {
      registrationXlsxImport(
        registrationDataImportData: $registrationDataImportData
      ) {
        registrationDataImport {
          name
          status
          numberOfHouseholds
          numberOfIndividuals
        }
      }
    }
    """

    APPROVE_REGISTRATION_DATA_IMPORT = """
    mutation ApproveRegistrationDataImportMutation($id: ID!) {
      approveRegistrationDataImport(id: $id) {
        registrationDataImport {
          status
        }
      }
    }
    """

    UNAPPROVE_REGISTRATION_DATA_IMPORT = """
    mutation UnapproveRegistrationDataImportMutation($id: ID!) {
      unapproveRegistrationDataImport(id: $id) {
        registrationDataImport {
          status
        }
      }
    }
    """

    MERGE_REGISTRATION_DATA_IMPORT = """
    mutation MergeRegistrationDataImportMutation($id: ID!) {
      mergeRegistrationDataImport(id: $id) {
        registrationDataImport {
          status
        }
      }
    }
    """

    @classmethod
    def setUpTestData(cls) -> None:
        partner = PartnerFactory(name="Partner")
        cls.user = UserFactory(partner=partner)
        create_afghanistan()
        cls.business_area_slug = "afghanistan"
        cls.business_area = BusinessArea.objects.get(slug=cls.business_area_slug)
        cls.program = ProgramFactory(status=Program.ACTIVE)
        cls.update_partner_access_to_program(partner, cls.program)

        img = io.BytesIO(Image.new("RGB", (60, 30), color="red").tobytes())

        cls.image = InMemoryUploadedFile(
            file=img,
            field_name="consent",
            name="consent.jpg",
            content_type="'image/jpeg'",
            size=60,
            charset=None,
        )

        xlsx_valid_file_path = (
            f"{settings.PROJECT_ROOT}/apps/registration_datahub/tests/test_file/new_reg_data_import.xlsx"
        )

        xlsx_invalid_file_path = f"{settings.PROJECT_ROOT}/apps/registration_datahub/tests/test_file/rdi_import_3_hh_missing_required_delivery_fields.xlsx"

        with open(xlsx_valid_file_path, "rb") as file:
            cls.valid_file = SimpleUploadedFile(file.name, file.read())
        with open(xlsx_invalid_file_path, "rb") as file:
            cls.invalid_file = SimpleUploadedFile(file.name, file.read())

    @parameterized.expand(
        [
            ("with_permission", [Permissions.RDI_IMPORT_DATA], True, True),
            ("with_permission_invalid_file", [Permissions.RDI_IMPORT_DATA], True, False),
            ("without_permission", [], False, False),
        ]
    )
    def test_registration_data_import_datahub_upload(
        self, _: Any, permissions: List[Permissions], should_have_import_data: bool, file_valid: bool
    ) -> None:
        self.create_user_role_with_permissions(self.user, permissions, self.business_area)
        if file_valid:
            file = self.valid_file
        else:
            file = self.invalid_file

        self.snapshot_graphql_request(
            request_string=self.UPLOAD_REGISTRATION_DATA_IMPORT_DATAHUB,
            context={
                "user": self.user,
                "headers": {
                    "Program": self.id_to_base64(self.program.id, "ProgramNode"),
                    "Business-Area": self.business_area.slug,
                },
            },
            variables={"file": file, "businessAreaSlug": self.business_area_slug},
        )

        if should_have_import_data and file_valid:
            import_data_obj = ImportData.objects.first()
            self.assertIn(
                "new_reg_data_import",
                import_data_obj.file.name,
            )

    @parameterized.expand(
        [
            (
                "with_permission",
                [Permissions.RDI_IMPORT_DATA],
            ),
            (
                "without_permission",
                [],
            ),
        ]
    )
    def test_registration_data_import_create(self, _: Any, permissions: List[Permissions]) -> None:
        program = ProgramFactory(status=Program.ACTIVE)

        import_data_obj = ImportData.objects.create(
            file=self.valid_file,
            number_of_households=3,
            number_of_individuals=6,
        )
        self.create_user_role_with_permissions(self.user, permissions, self.business_area)
        self.update_partner_access_to_program(self.user.partner, program)
        self.snapshot_graphql_request(
            request_string=self.CREATE_REGISTRATION_DATA_IMPORT,
            context={"user": self.user, "headers": {"Program": self.id_to_base64(program.id, "ProgramNode")}},
            variables={
                "registrationDataImportData": {
                    "importDataId": self.id_to_base64(import_data_obj.id, "ImportDataNode"),
                    "name": "New Import of Data 123",
                    "businessAreaSlug": self.business_area_slug,
                }
            },
        )

    def test_registration_data_import_create_validate_import_data(self) -> None:
        program = ProgramFactory(status=Program.ACTIVE)

        import_data_obj = ImportData.objects.create(
            file=self.valid_file,
            number_of_households=3,
            number_of_individuals=6,
            status=ImportData.STATUS_VALIDATION_ERROR,
        )
        self.create_user_role_with_permissions(self.user, [Permissions.RDI_IMPORT_DATA], self.business_area)
        self.update_partner_access_to_program(self.user.partner, program)
        self.snapshot_graphql_request(
            request_string=self.CREATE_REGISTRATION_DATA_IMPORT,
            context={"user": self.user, "headers": {"Program": self.id_to_base64(program.id, "ProgramNode")}},
            variables={
                "registrationDataImportData": {
                    "importDataId": self.id_to_base64(import_data_obj.id, "ImportDataNode"),
                    "name": "New Import of Data 123",
                    "businessAreaSlug": self.business_area_slug,
                    "allowDeliveryMechanismsValidationErrors": False,
                }
            },
        )
