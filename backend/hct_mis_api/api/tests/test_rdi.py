import base64
from pathlib import Path
from typing import Dict

from rest_framework import status
from rest_framework.reverse import reverse

from hct_mis_api.api.models import Grant
from hct_mis_api.api.tests.base import HOPEApiTestCase
from hct_mis_api.apps.core.utils import IDENTIFICATION_TYPE_TO_KEY_MAPPING
from hct_mis_api.apps.household.models import (
    HEAD,
    IDENTIFICATION_TYPE_BIRTH_CERTIFICATE,
    NON_BENEFICIARY,
    ROLE_PRIMARY,
)
from hct_mis_api.apps.program.fixtures import ProgramFactory
from hct_mis_api.apps.program.models import Program
from hct_mis_api.apps.registration_data.models import (
    RegistrationDataImport,
    RegistrationDataImportDatahub,
)
from hct_mis_api.apps.registration_datahub.models import (
    COLLECT_TYPE_FULL,
    ImportedDocumentType,
    ImportedHousehold,
)


class CreateRDITests(HOPEApiTestCase):
    databases = {"default", "registration_datahub"}
    user_permissions = [Grant.API_RDI_CREATE]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.url = reverse("api:rdi-create", args=[cls.business_area.slug])
        cls.program = ProgramFactory.create(status=Program.DRAFT, business_area=cls.business_area)

    def test_create_rdi(self) -> None:
        data = {
            "name": "aaaa",
            "collect_data_policy": "FULL",
            "program": str(self.program.id),
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, str(response.json()))
        hrdi = RegistrationDataImportDatahub.objects.filter(name="aaaa").first()
        self.assertTrue(hrdi)

        rdi = RegistrationDataImport.objects.filter(datahub_id=str(hrdi.pk)).first()
        self.assertIsNotNone(rdi)
        self.assertEqual(rdi.program, self.program)
        self.assertEqual(rdi.status, RegistrationDataImport.LOADING)

        self.assertEqual(response.json()["id"], str(hrdi.id))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, str(response.json()))


class PushToRDITests(HOPEApiTestCase):
    databases = {"default", "registration_datahub"}
    user_permissions = [Grant.API_RDI_CREATE]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        ImportedDocumentType.objects.create(
            key=IDENTIFICATION_TYPE_TO_KEY_MAPPING[IDENTIFICATION_TYPE_BIRTH_CERTIFICATE], label="--"
        )
        cls.program = ProgramFactory.create(status=Program.DRAFT, business_area=cls.business_area)
        cls.rdi = RegistrationDataImportDatahub.objects.create(
            business_area_slug=cls.business_area.slug, import_done=RegistrationDataImportDatahub.LOADING
        )
        cls.rdi2: RegistrationDataImport = RegistrationDataImport.objects.create(
            business_area=cls.business_area,
            number_of_individuals=0,
            number_of_households=0,
            datahub_id=cls.rdi.pk,
            status=RegistrationDataImport.LOADING,
            program=cls.program,
        )
        cls.url = reverse("api:rdi-push", args=[cls.business_area.slug, str(cls.rdi.id)])

    def test_push(self) -> None:
        image = Path(__file__).parent / "logo.png"
        base64_encoded_data = base64.b64encode(image.read_bytes())
        input_data = [
            {
                "residence_status": "",
                "village": "village1",
                "country": "AF",
                "members": [
                    {
                        "relationship": HEAD,
                        "full_name": "James Head #1",
                        "birth_date": "2000-01-01",
                        "sex": "MALE",
                        "role": "",
                        "documents": [
                            {
                                "document_number": 10,
                                "image": base64_encoded_data,
                                "doc_date": "2010-01-01",
                                "country": "AF",
                                "type": IDENTIFICATION_TYPE_TO_KEY_MAPPING[IDENTIFICATION_TYPE_BIRTH_CERTIFICATE],
                            }
                        ],
                    },
                    {
                        "relationship": NON_BENEFICIARY,
                        "full_name": "Mary Primary #1",
                        "birth_date": "2000-01-01",
                        "role": ROLE_PRIMARY,
                        "sex": "FEMALE",
                    },
                ],
                "collect_individual_data": COLLECT_TYPE_FULL,
                "size": 1,
            }
        ]
        response = self.client.post(self.url, input_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, str(response.json()))

        data: Dict = response.json()
        hrdi = RegistrationDataImportDatahub.objects.filter(id=data["id"]).first()
        self.assertIsNotNone(hrdi)

        hh = ImportedHousehold.objects.filter(registration_data_import=hrdi, village="village1").first()
        self.assertIsNotNone(hh)
        self.assertIsNotNone(hh.head_of_household)
        self.assertIsNotNone(hh.primary_collector)
        self.assertIsNone(hh.alternate_collector)
        self.assertEqual(hh.collect_individual_data, COLLECT_TYPE_FULL)
        self.assertEqual(hh.program_id, self.program.id)

        self.assertEqual(hh.primary_collector.full_name, "Mary Primary #1")
        self.assertEqual(hh.head_of_household.full_name, "James Head #1")

        self.assertEqual(hh.primary_collector.program_id, self.program.id)
        self.assertEqual(hh.head_of_household.program_id, self.program.id)

        self.assertEqual(data["households"], 1)
        self.assertEqual(data["individuals"], 2)

    def test_push_fail_if_not_loading(self) -> None:
        rdi = RegistrationDataImportDatahub.objects.create(
            business_area_slug=self.business_area.slug,
            import_done=RegistrationDataImportDatahub.NOT_STARTED,
        )
        url = reverse("api:rdi-push", args=[self.business_area.slug, str(rdi.id)])
        response = self.client.post(url, [], format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.data


class CompleteRDITests(HOPEApiTestCase):
    databases = {"default", "registration_datahub"}
    user_permissions = [Grant.API_RDI_CREATE]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.program = ProgramFactory.create(status=Program.DRAFT, business_area=cls.business_area)
        cls.rdi = RegistrationDataImportDatahub.objects.create(
            business_area_slug=cls.business_area.slug, import_done=RegistrationDataImport.LOADING
        )
        cls.rdi2: RegistrationDataImport = RegistrationDataImport.objects.create(
            business_area=cls.business_area,
            number_of_individuals=0,
            number_of_households=0,
            datahub_id=cls.rdi.pk,
            status=RegistrationDataImport.LOADING,
            program=cls.program,
        )
        assert cls.rdi.linked_rdi == cls.rdi2

        cls.url = reverse("api:rdi-complete", args=[cls.business_area.slug, str(cls.rdi.id)])

    def test_complete(self) -> None:
        data = {}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.json()))
        data = response.json()
        self.assertDictEqual(data[0], {"id": str(self.rdi.id), "status": "DONE"})
        self.assertDictEqual(data[1], {"id": str(self.rdi2.id), "status": "IN_REVIEW"})
        self.rdi2.refresh_from_db()
        self.assertEqual(self.rdi2.status, RegistrationDataImport.IN_REVIEW)
