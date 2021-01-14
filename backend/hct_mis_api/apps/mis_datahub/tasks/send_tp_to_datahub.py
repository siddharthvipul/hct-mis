from django.db import transaction
from django.db.models import Q, F, Prefetch
from django.utils import timezone

from hct_mis_api.apps.core.utils import nested_getattr
from hct_mis_api.apps.household.models import (
    Individual,
    IndividualRoleInHousehold,
    Household,
)
from hct_mis_api.apps.mis_datahub import models as dh_mis_models
from hct_mis_api.apps.targeting.models import TargetPopulation, HouseholdSelection


class SendTPToDatahubTask:
    MAPPING_TP_DICT = {
        "mis_id": "id",
        "name": "name",
        "active_households": "final_list_total_households",
        "program_mis_id": "program.id",
        "targeting_criteria": "targeting_criteria_string",
    }
    MAPPING_PROGRAM_DICT = {
        "mis_id": "id",
        "name": "name",
        "business_area": "business_area.code",
        "scope": "scope",
        "start_date": "start_date",
        "end_date": "end_date",
        "description": "description",
        "individual_data_needed": "individual_data_needed",
    }

    MAPPING_HOUSEHOLD_DICT = {
        "mis_id": "id",
        "unicef_id": "unicef_id",
        "status": "status",
        "household_size": "size",
        "address": "address",
        "admin1": "admin_area.title",
        "admin2": "admin_area.parent.title",
        "residence_status": "residence_status",
        "registration_date": "last_registration_date",
        "country": "country.alpha3",
    }
    MAPPING_INDIVIDUAL_DICT = {
        "mis_id": "id",
        "unicef_id": "unicef_id",
        "status": "status",
        "full_name": "full_name",
        "family_name": "family_name",
        "given_name": "given_name",
        "middle_name": "middle_name",
        "sex": "sex",
        "date_of_birth": "birth_date",
        "estimated_date_of_birth": "estimated_birth_date",
        "relationship": "relationship",
        "marital_status": "marital_status",
        "phone_number": "phone_no",
        "household_mis_id": "household.id",
        "pregnant": "pregnant",
    }
    MAPPING_DOCUMENT_DICT = {
        "mis_id": "id",
        "number": "document_number",
        "individual_mis_id": "individual.id",
        "type": "type.type",
    }

    def execute(self):
        target_populations = TargetPopulation.objects.filter(
            status=TargetPopulation.STATUS_FINALIZED, sent_to_datahub=False
        )
        for target_population in target_populations:
            self.send_tp(target_population)

    @staticmethod
    def remove_duplicated_households(households_to_create):
        households_to_create_deduped_dict = {household.mis_id: household for household in households_to_create}
        households_to_create_deduped = [value for key, value in households_to_create_deduped_dict.items()]
        return households_to_create_deduped

    @transaction.atomic(using="default")
    @transaction.atomic(using="cash_assist_datahub_mis")
    def send_tp(self, target_population):
        households_to_bulk_create = []
        collectors_households_to_bulk_create = []
        individuals_to_bulk_create = []
        documents_to_bulk_create = []
        tp_entries_to_bulk_create = []

        program = target_population.program
        dh_session = dh_mis_models.Session(
            source=dh_mis_models.Session.SOURCE_MIS,
            status=dh_mis_models.Session.STATUS_READY,
            business_area=program.business_area.code,
        )
        dh_session.save()
        target_population_selections = HouseholdSelection.objects.filter(
            target_population__id=target_population.id, final=True
        )
        households = target_population.final_list.filter()
        # individuals = Individual.objects.filter(
        #     household__id__in=target_population.households.values_list(
        #         "id", flat=True
        #     )
        # ).filter(
        #     Q(last_sync_at__isnull=True)
        #     | Q(last_sync_at__lte=F("updated_at"))
        # )

        if program.last_sync_at is None or program.last_sync_at < program.updated_at:
            dh_program = self.send_program(program)
            dh_program.session = dh_session
            dh_program.save()
            program.last_sync_at = timezone.now()
            program.save(update_fields=["last_sync_at"])
        dh_target = self.send_target_population(target_population)
        dh_target.session = dh_session
        dh_target.save()
        household_ids = households.values_list("id", flat=True)

        for household in households:
            dh_household, dh_collectors_households, dh_individuals = self.send_household(
                household,
                program,
                dh_session,
                household_ids,
            )
            collectors_households_to_bulk_create.extend(dh_collectors_households)
            if dh_household is not None:
                households_to_bulk_create.append(dh_household)
            individuals_to_bulk_create.extend(dh_individuals)

        for selection in target_population_selections:
            dh_entry = self.send_target_entry(selection)
            dh_entry.session = dh_session
            tp_entries_to_bulk_create.append(dh_entry)
        collectors_households_to_bulk_create = SendTPToDatahubTask.remove_duplicated_households(
            collectors_households_to_bulk_create
        )
        households_to_bulk_create = SendTPToDatahubTask.remove_duplicated_households(households_to_bulk_create)
        households_to_bulk_create_mis_ids = [str(x.mis_id) for x in households_to_bulk_create]
        collectors_households_to_bulk_create = [
            dh_collector_household
            for dh_collector_household in collectors_households_to_bulk_create
            if str(dh_collector_household.mis_id) not in households_to_bulk_create_mis_ids
        ]
        dh_mis_models.Household.objects.bulk_create(households_to_bulk_create)
        dh_mis_models.Household.objects.bulk_create(collectors_households_to_bulk_create)
        dh_mis_models.Individual.objects.bulk_create(individuals_to_bulk_create)
        dh_mis_models.Document.objects.bulk_create(documents_to_bulk_create)
        dh_mis_models.TargetPopulationEntry.objects.bulk_create(tp_entries_to_bulk_create)
        target_population.sent_to_datahub = True
        target_population.save()
        households.update(last_sync_at=timezone.now())

    def build_arg_dict(self, model_object, mapping_dict):
        args = {}
        for key in mapping_dict:
            args[key] = nested_getattr(model_object, mapping_dict[key], None)
        return args

    def send_program(self, program):
        dh_program_args = self.build_arg_dict(program, SendTPToDatahubTask.MAPPING_PROGRAM_DICT)

        dh_program = dh_mis_models.Program(**dh_program_args)
        return dh_program

    def send_target_population(self, target_population):
        dh_tp_args = self.build_arg_dict(target_population, SendTPToDatahubTask.MAPPING_TP_DICT)
        dh_target = dh_mis_models.TargetPopulation(**dh_tp_args)
        return dh_target

    def send_individual(self, individual, dh_household, dh_session, household_ids):
        dh_individual_args = self.build_arg_dict(individual, SendTPToDatahubTask.MAPPING_INDIVIDUAL_DICT)
        dh_individual = dh_mis_models.Individual(**dh_individual_args)
        dh_individual.household = dh_household

        for document in individual.documents.all():
            dh_document_args = self.build_arg_dict(document, SendTPToDatahubTask.MAPPING_DOCUMENT_DICT)
            dh_document, _ = dh_mis_models.Document.objects.get_or_create(
                **dh_document_args,
                session=dh_session,
            )

        dh_individual.unhcr_id = self.get_unhcr_individual_id(individual)
        roles = individual.households_and_roles.filter(household__id__in=household_ids)
        for role in roles:
            dh_mis_models.IndividualRoleInHousehold.objects.get_or_create(
                role=role.role,
                household_mis_id=role.household.id,
                individual_mis_id=role.individual.id,
                session=dh_session,
            )

        dh_individual.session = dh_session
        return dh_individual

    def send_household(self, household, program, dh_session, household_ids):
        dh_household_args = self.build_arg_dict(household, SendTPToDatahubTask.MAPPING_HOUSEHOLD_DICT)
        dh_collectors_households = []
        dh_household = None
        is_creating = False
        if household.last_sync_at is None or household.last_sync_at <= household.updated_at:
            dh_household = dh_mis_models.Household(**dh_household_args)
            dh_household.unhcr_id = self.get_unhcr_household_id(household)
            dh_household.session = dh_session
            is_creating = True
        else:
            dh_household = dh_mis_models.Household.objects.filter(mis_id=household.id).last()

        head_of_household = household.head_of_household
        collectors_ids = list(
            household.representatives.filter(
                Q(last_sync_at__isnull=True) | Q(last_sync_at__lte=F("updated_at"))
            ).values_list("id", flat=True)
        )
        collectors_household_ids = list(
            household.representatives.exclude(household_id__in=household_ids)
            .values_list("household_id", flat=True)
            .distinct("household_id")
        )
        collectors_households = Household.objects.filter(id__in=collectors_household_ids)
        for collectors_household in collectors_households:
            collectors_dh_household_args = self.build_arg_dict(
                collectors_household, SendTPToDatahubTask.MAPPING_HOUSEHOLD_DICT
            )
            collectors_dh_household = dh_mis_models.Household(**collectors_dh_household_args)
            collectors_dh_household.session = dh_session
            dh_collectors_households.append(collectors_dh_household)
        ids = {head_of_household.id, *collectors_ids}
        individuals_to_create = []
        if program.individual_data_needed:
            individuals = household.individuals.all()
            for individual in individuals:
                if self.should_send_individual(individual, household):
                    dh_individual = self.send_individual(
                        individual,
                        dh_household,
                        dh_session,
                        household_ids,
                    )
                    dh_individual.session = dh_session
                    individuals_to_create.append(dh_individual)
        else:
            individuals = (
                Individual.objects.filter(id__in=ids)
                .filter(Q(last_sync_at__isnull=True) | Q(last_sync_at__lte=F("updated_at")))
                .prefetch_related(
                    Prefetch(
                        "households_and_roles",
                        queryset=IndividualRoleInHousehold.objects.filter(household=household.id),
                    )
                )
            )
            for individual in individuals:
                if self.should_send_individual(individual, household):
                    dh_individual = self.send_individual(
                        individual,
                        dh_household,
                        dh_session,
                        household_ids,
                    )
                    dh_individual.session = dh_session
                    individuals_to_create.append(dh_individual)
        individuals.update(last_sync_at=timezone.now())
        return dh_household if is_creating else None, dh_collectors_households, individuals_to_create

    def should_send_individual(self, individual, household):
        is_not_synced = individual.last_sync_at is None or individual.last_sync_at <= individual.updated_at
        is_allowed_to_share = household.business_area.has_data_sharing_agreement
        return is_not_synced and is_allowed_to_share

    def send_target_entry(self, target_population_selection):
        household_unhcr_id = self.get_unhcr_household_id(target_population_selection.household)
        return dh_mis_models.TargetPopulationEntry(
            target_population_mis_id=target_population_selection.target_population.id,
            household_mis_id=target_population_selection.household.id,
            household_unhcr_id=household_unhcr_id,
            vulnerability_score=target_population_selection.vulnerability_score,
        )

    def get_unhcr_individual_id(self, individual):
        identity = individual.identities.filter(agency__type="UNHCR").first()
        if identity is not None:
            return identity.number
        return None

    def get_unhcr_household_id(self, household):
        return household.unhcr_id
