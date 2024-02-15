from rest_framework.reverse import reverse

from hct_mis_api.api.models import Grant
from hct_mis_api.api.tests.base import HOPEApiTestCase
from hct_mis_api.apps.program.models import Program


class CreateProgramTests(HOPEApiTestCase):
    databases = {"default"}
    user_permissions = [Grant.API_PROGRAM_CREATE]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.create_url = reverse("api:program-create", args=[cls.business_area.slug])
        cls.list_url = reverse("api:program-list", args=[cls.business_area.slug])

    def test_create_program(self) -> None:
        data = {
            "name": "Program #1",
            "start_date": "2022-09-27",
            "end_date": "2022-09-27",
            "budget": "10000",
            "frequency_of_payments": "ONE_OFF",
            "sector": "CHILD_PROTECTION",
            "cash_plus": True,
            "population_goal": 101,
        }
        response = self.client.post(self.create_url, data, format="json")
        data = response.json()
        if not (program := Program.objects.filter(name="Program #1").first()):
            self.fail("Program was not present")
        self.assertTrue(program)
        self.assertDictEqual(
            data,
            {
                "budget": "10000.00",
                "cash_plus": True,
                "end_date": "2022-09-27",
                "frequency_of_payments": "ONE_OFF",
                "id": str(program.id),
                "name": "Program #1",
                "population_goal": 101,
                "sector": "CHILD_PROTECTION",
                "start_date": "2022-09-27",
            },
        )

        self.assertEqual(program.business_area, self.business_area)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertDictEqual(
            response.json()[0],
            {
                "budget": "10000.00",
                "cash_plus": True,
                "end_date": "2022-09-27",
                "frequency_of_payments": "ONE_OFF",
                "id": str(program.id),
                "name": "Program #1",
                "population_goal": 101,
                "sector": "CHILD_PROTECTION",
                "start_date": "2022-09-27",
            },
        )
