from unittest import mock

from django.test import TestCase

from hct_mis_api.apps.account.fixtures import UserFactory
from hct_mis_api.apps.core.field_attributes.core_fields_attributes import (
    CORE_FIELDS_ATTRIBUTES,
    FieldFactory,
)
from hct_mis_api.apps.core.field_attributes.fields_types import (
    _DELIVERY_MECHANISM_DATA,
    _HOUSEHOLD,
    _INDIVIDUAL,
)
from hct_mis_api.apps.core.fixtures import create_afghanistan
from hct_mis_api.apps.core.models import BusinessArea
from hct_mis_api.apps.grievance.models import (
    GrievanceTicket,
    TicketIndividualDataUpdateDetails,
)
from hct_mis_api.apps.household.fixtures import HouseholdFactory, IndividualFactory
from hct_mis_api.apps.household.models import LOT_DIFFICULTY
from hct_mis_api.apps.payment.delivery_mechanisms import DeliveryMechanismChoices
from hct_mis_api.apps.payment.fixtures import DeliveryMechanismDataFactory
from hct_mis_api.apps.payment.models import DeliveryMechanismData
from hct_mis_api.apps.program.fixtures import ProgramFactory


class TestDeliveryMechanismDataModel(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        create_afghanistan()
        cls.program1 = ProgramFactory()
        cls.user = UserFactory.create()
        cls.ind = IndividualFactory(household=None, program=cls.program1)
        cls.ind2 = IndividualFactory(household=None, program=cls.program1)
        cls.hh = HouseholdFactory(head_of_household=cls.ind)
        cls.ind.household = cls.hh
        cls.ind.save()
        cls.ind2.household = cls.hh
        cls.ind2.save()

        cls.all_fields = FieldFactory(CORE_FIELDS_ATTRIBUTES).to_dict_by("name")

    def test_str(self) -> None:
        dmd = DeliveryMechanismDataFactory(individual=self.ind)
        self.assertEqual(str(dmd), f"[{dmd.id}] {dmd.individual} - {dmd.delivery_mechanism}")

    def test_get_associated_object(self) -> None:
        dmd = DeliveryMechanismDataFactory(data={"test": "test"}, individual=self.ind)
        self.assertEqual(dmd.get_associated_object(_DELIVERY_MECHANISM_DATA), dmd.data)
        self.assertEqual(dmd.get_associated_object(_HOUSEHOLD), dmd.individual.household)
        self.assertEqual(dmd.get_associated_object(_INDIVIDUAL), dmd.individual)

    def test_delivery_data(self) -> None:
        dmd = DeliveryMechanismDataFactory(data={"name_of_cardholder_atm_card": "test"}, individual=self.ind)
        delivery_mechanism_fields = [
            self.all_fields["full_name"],
            self.all_fields["number_of_children"],
            self.all_fields["name_of_cardholder_atm_card"],
        ]
        self.hh.number_of_children = 1
        self.hh.save()

        with mock.patch.object(dmd, "delivery_mechanism_fields", delivery_mechanism_fields):
            self.assertEqual(
                dmd.delivery_data,
                {
                    "full_name": dmd.individual.full_name,
                    "number_of_children": 1,
                    "name_of_cardholder_atm_card": "test",
                },
            )

    def test_validate(self) -> None:
        dmd = DeliveryMechanismDataFactory(data={"test": "test"}, individual=self.ind)
        dmd.individual.household.number_of_children = None
        dmd.individual.household.save()
        dmd.individual.seeing_disability = ""
        dmd.individual.save()
        required_fields = [
            self.all_fields["seeing_disability"],
            self.all_fields["number_of_children"],
            self.all_fields["name_of_cardholder_atm_card"],
        ]
        with mock.patch.object(dmd, "required_fields", required_fields):
            dmd.validate()
            self.assertEqual(
                dmd.validation_errors,
                {
                    "seeing_disability": "Missing required payment data",
                    "number_of_children": "Missing required payment data",
                    "name_of_cardholder_atm_card": "Missing required payment data",
                },
            )
            self.assertEqual(dmd.is_valid, False)

    def test_update_unique_fields(self) -> None:
        unique_fields = [
            self.all_fields["seeing_disability"],
            self.all_fields["name_of_cardholder_atm_card"],
        ]

        dmd_1 = DeliveryMechanismDataFactory(
            data={"name_of_cardholder_atm_card": "test"}, individual=self.ind, is_valid=True
        )
        dmd_1.individual.seeing_disability = LOT_DIFFICULTY
        dmd_1.individual.save()

        dmd_2 = DeliveryMechanismDataFactory(
            data={"name_of_cardholder_atm_card": "test2"}, individual=self.ind2, is_valid=True
        )
        dmd_2.individual.seeing_disability = LOT_DIFFICULTY
        dmd_2.individual.save()

        with mock.patch.object(dmd_1, "unique_fields", unique_fields):
            dmd_1.update_unique_field()
            self.assertEqual(dmd_1.is_valid, True)
            self.assertIsNotNone(dmd_1.unique_key)
            self.assertEqual(dmd_1.validation_errors, {})

    def test_update_unique_fields_possible_duplicates(self) -> None:
        unique_fields = [
            self.all_fields["seeing_disability"],
            self.all_fields["name_of_cardholder_atm_card"],
        ]

        dmd_1 = DeliveryMechanismDataFactory(individual=self.ind, is_valid=True)
        dmd_2 = DeliveryMechanismDataFactory(individual=self.ind2, is_valid=True)

        delivery_data = {
            "seeing_disability": LOT_DIFFICULTY,
            "name_of_cardholder_atm_card": "test",
        }

        with mock.patch.object(dmd_1, "unique_fields", unique_fields):
            with mock.patch.object(dmd_2, "unique_fields", unique_fields):
                with mock.patch.object(dmd_1, "delivery_data", delivery_data):
                    with mock.patch.object(dmd_2, "delivery_data", delivery_data):
                        dmd_1.update_unique_field()
                        dmd_1.save()
                        self.assertEqual(dmd_1.is_valid, True)
                        self.assertIsNotNone(dmd_1.unique_key)
                        self.assertEqual(dmd_1.validation_errors, {})
                        self.assertEqual(dmd_1.possible_duplicate_of, None)

                        dmd_2.update_unique_field()
                        dmd_2.save()
                        self.assertEqual(dmd_2.is_valid, False)
                        self.assertIsNone(dmd_2.unique_key)
                        self.assertEqual(
                            dmd_2.validation_errors,
                            {
                                "seeing_disability": "Payment data not unique across Program",
                                "name_of_cardholder_atm_card": "Payment data not unique across Program",
                            },
                        )
                        self.assertEqual(dmd_2.possible_duplicate_of, dmd_1)

    def test_delivery_mechanism_fields(self) -> None:
        dmd = DeliveryMechanismDataFactory(
            individual=self.ind, delivery_mechanism=DeliveryMechanismChoices.DELIVERY_TYPE_ATM_CARD
        )
        self.assertEqual(
            [field["name"] for field in dmd.delivery_mechanism_fields],
            [
                "full_name",
                "card_number_atm_card",
                "card_expiry_date_atm_card",
                "name_of_cardholder_atm_card",
            ],
        )

    def test_required_fields(self) -> None:
        dmd = DeliveryMechanismDataFactory(
            individual=self.ind, delivery_mechanism=DeliveryMechanismChoices.DELIVERY_TYPE_ATM_CARD
        )
        self.assertEqual(
            [field["name"] for field in dmd.required_fields],
            [
                "card_number_atm_card",
                "card_expiry_date_atm_card",
                "name_of_cardholder_atm_card",
            ],
        )

    def test_unique_fields(self) -> None:
        dmd = DeliveryMechanismDataFactory(
            individual=self.ind, delivery_mechanism=DeliveryMechanismChoices.DELIVERY_TYPE_ATM_CARD
        )
        self.assertEqual(
            [field["name"] for field in dmd.unique_fields],
            [
                "card_number_atm_card",
                "card_expiry_date_atm_card",
                "name_of_cardholder_atm_card",
            ],
        )

    def test_get_all_delivery_mechanisms_fields(self) -> None:
        fields = DeliveryMechanismData.get_all_delivery_mechanisms_fields()
        self.assertEqual(
            [fields["name"] for fields in fields],
            [
                "full_name",
                "card_number_atm_card",
                "card_expiry_date_atm_card",
                "name_of_cardholder_atm_card",
                "card_number_deposit_to_card",
                "delivery_phone_number_mobile_money",
                "provider_mobile_money",
                "bank_name_transfer_to_account",
                "bank_account_number_transfer_to_account",
                "mobile_phone_number_cash_over_the_counter",
                "wallet_name_transfer_to_digital_wallet",
                "blockchain_name_transfer_to_digital_wallet",
                "wallet_address_transfer_to_digital_wallet",
            ],
        )

    def test_get_required_delivery_mechanism_fields(self) -> None:
        fields = DeliveryMechanismData.get_required_delivery_mechanism_fields(
            DeliveryMechanismChoices.DELIVERY_TYPE_ATM_CARD
        )
        self.assertEqual(
            [fields["name"] for fields in fields],
            [
                "card_number_atm_card",
                "card_expiry_date_atm_card",
                "name_of_cardholder_atm_card",
            ],
        )

    def test_get_delivery_mechanism_fields(self) -> None:
        fields = DeliveryMechanismData.get_delivery_mechanism_fields(DeliveryMechanismChoices.DELIVERY_TYPE_ATM_CARD)
        self.assertEqual(
            [fields["name"] for fields in fields],
            [
                "full_name",
                "card_number_atm_card",
                "card_expiry_date_atm_card",
                "name_of_cardholder_atm_card",
            ],
        )

    def test_get_grievance_ticket_payload_for_errors(self) -> None:
        dmd = DeliveryMechanismDataFactory(
            individual=self.ind,
            validation_errors={
                "full_name": "Missing required payment data",
                "number_of_children": "Missing required payment data",
                "name_of_cardholder_atm_card": "Missing required payment data",
            },
        )
        self.assertEqual(
            dmd.get_grievance_ticket_payload_for_errors(),
            {
                "id": str(dmd.id),
                "label": dmd.delivery_mechanism,
                "approve_status": False,
                "data_fields": [
                    {
                        "name": "full_name",
                        "value": None,
                        "previous_value": dmd.individual.full_name,
                    },
                    {
                        "name": "number_of_children",
                        "value": None,
                        "previous_value": None,
                    },
                    {
                        "name": "name_of_cardholder_atm_card",
                        "value": None,
                        "previous_value": None,
                    },
                ],
            },
        )

    def test_revalidate_for_grievance_ticket(self) -> None:
        ba = BusinessArea.objects.get(slug="afghanistan")
        grievance_ticket = GrievanceTicket.objects.create(
            category=GrievanceTicket.CATEGORY_DATA_CHANGE,
            issue_type=GrievanceTicket.ISSUE_TYPE_INDIVIDUAL_DATA_CHANGE_DATA_UPDATE,
            admin2=self.ind.household.admin2,
            business_area=ba,
            description="description",
            comments="",
        )
        individual_data_update_ticket = TicketIndividualDataUpdateDetails.objects.create(
            individual_data={"delivery_mechanism_data_to_edit": []},
            individual=self.ind,
            ticket=grievance_ticket,
        )
        dmd = DeliveryMechanismDataFactory(
            individual=self.ind,
            is_valid=False,
            validation_errors={
                "full_name": "Missing required payment data",
                "name_of_cardholder_atm_card": "Missing required payment data",
            },
            delivery_mechanism=DeliveryMechanismChoices.DELIVERY_TYPE_ATM_CARD,
        )

        with mock.patch.object(dmd, "validate"):
            dmd.revalidate_for_grievance_ticket(grievance_ticket)
            grievance_ticket.refresh_from_db()
            self.assertEqual(grievance_ticket.status, GrievanceTicket.STATUS_IN_PROGRESS)
            self.assertEqual(
                grievance_ticket.description,
                "Missing required fields ['full_name', 'name_of_cardholder_atm_card'] values for delivery mechanism ATM Card",
            )
            self.assertEqual(
                individual_data_update_ticket.individual_data,
                {
                    "delivery_mechanism_data_to_edit": [
                        {
                            "id": str(dmd.id),
                            "label": dmd.delivery_mechanism,
                            "approve_status": False,
                            "data_fields": [
                                {
                                    "name": "full_name",
                                    "value": None,
                                    "previous_value": dmd.individual.full_name,
                                },
                                {
                                    "name": "name_of_cardholder_atm_card",
                                    "value": None,
                                    "previous_value": None,
                                },
                            ],
                        }
                    ]
                },
            )

            dmd.is_valid = True
            dmd.validation_errors = {}
            dmd.save()

            def update_unique_field_side_effect() -> None:
                dmd.unique_key = None
                dmd.is_valid = False
                dmd.validation_errors = {
                    "aaa": "Payment data not unique across Program",
                    "bbb": "Payment data not unique across Program",
                }
                dmd.possible_duplicate_of = dmd
                dmd.save()

            with mock.patch.object(dmd, "update_unique_field", side_effect=update_unique_field_side_effect):
                dmd.revalidate_for_grievance_ticket(grievance_ticket)

                self.assertEqual(grievance_ticket.status, GrievanceTicket.STATUS_IN_PROGRESS)
                self.assertEqual(
                    grievance_ticket.description,
                    f"Fields not unique ['aaa', 'bbb'] across program"
                    f" for delivery mechanism {dmd.delivery_mechanism}, possible duplicate of {dmd}",
                )
                self.assertEqual(
                    individual_data_update_ticket.individual_data,
                    {
                        "delivery_mechanism_data_to_edit": [
                            {
                                "id": str(dmd.id),
                                "label": dmd.delivery_mechanism,
                                "approve_status": False,
                                "data_fields": [
                                    {
                                        "name": "full_name",
                                        "value": None,
                                        "previous_value": dmd.individual.full_name,
                                    },
                                    {
                                        "name": "name_of_cardholder_atm_card",
                                        "value": None,
                                        "previous_value": None,
                                    },
                                ],
                            }
                        ]
                    },
                )
