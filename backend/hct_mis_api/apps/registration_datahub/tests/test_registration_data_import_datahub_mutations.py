import io

from PIL import Image
from django.conf import settings
from django.core.files.uploadedfile import (
    InMemoryUploadedFile,
    SimpleUploadedFile,
)
from django.core.management import call_command

from account.fixtures import UserFactory
from core.base_test_case import APITestCase
from registration_datahub.models import ImportData


class TestRegistrationDataImportDatahubMutations(APITestCase):
    multi_db = True

    UPLOAD_REGISTRATION_DATA_IMPORT_DATAHUB = """
    mutation UploadImportDataXLSXFile(
      $file: Upload!, $businessAreaSlug: String!
    ) {
      uploadImportDataXlsxFile(
        file: $file, businessAreaSlug: $businessAreaSlug
      ) {
        importData {
          numberOfHouseholds
          numberOfIndividuals
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

    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        call_command("loadbusinessareas")

        img = io.BytesIO(Image.new("RGB", (60, 30), color="red").tobytes())

        self.image = InMemoryUploadedFile(
            file=img,
            field_name="consent",
            name="consent.jpg",
            content_type="'image/jpeg'",
            size=(60, 30),
            charset=None,
        )

        xlsx_valid_file_path = f"{settings.PROJECT_ROOT}/apps/registration_datahub/tests/test_file/new_reg_data_import.xlsx"

        with open(xlsx_valid_file_path, "rb") as file:
            self.valid_file = SimpleUploadedFile(file.name, file.read())

    def test_registration_data_import_datahub_upload(self):
        self.snapshot_graphql_request(
            request_string=self.UPLOAD_REGISTRATION_DATA_IMPORT_DATAHUB,
            context={"user": self.user},
            variables={
                "file": self.valid_file,
                "businessAreaSlug": "afghanistan",
            },
        )

        import_data_obj = ImportData.objects.first()
        self.assertIn(
            "new_reg_data_import", import_data_obj.file.name,
        )

    def test_registration_data_import_create(self):
        import_data_obj = ImportData.objects.create(
            file=self.valid_file,
            number_of_households=3,
            number_of_individuals=6,
        )

        self.snapshot_graphql_request(
            request_string=self.CREATE_REGISTRATION_DATA_IMPORT,
            context={"user": self.user},
            variables={
                "registrationDataImportData": {
                    "importDataId": self.id_to_base64(
                        import_data_obj.id, "ImportData"
                    ),
                    "name": "New Import of Data 123",
                    "businessAreaSlug": "afghanistan",
                }
            },
        )
