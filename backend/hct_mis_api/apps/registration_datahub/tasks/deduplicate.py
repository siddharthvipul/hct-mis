import json
import logging

from constance import config
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django_countries.fields import Country

from hct_mis_api.apps.activity_log.models import log_create
from hct_mis_api.apps.core.utils import to_dict
from hct_mis_api.apps.household.documents import IndividualDocument
from hct_mis_api.apps.household.elasticsearch_utils import populate_index
from hct_mis_api.apps.household.models import (
    Individual,
    DUPLICATE,
    NEEDS_ADJUDICATION,
    UNIQUE,
    NOT_PROCESSED,
    DUPLICATE_IN_BATCH,
    UNIQUE_IN_BATCH,
)
from hct_mis_api.apps.registration_data.models import RegistrationDataImport
from hct_mis_api.apps.registration_datahub.documents import ImportedIndividualDocument
from hct_mis_api.apps.registration_datahub.models import ImportedIndividual

log = logging.getLogger(__name__)


class DeduplicateTask:
    """
    WARNING: when deduplication for all business areas will be enabled we need to find a way to block
    other task from interfering with elasticsearch indexes
    (disabling parallel)
    """

    FUZZINESS = "AUTO:3,6"
    business_area = None

    @classmethod
    def _prepare_query_dict(cls, individual, fields, min_score):
        fields_meta = {
            "birth_date": {"boost": 2},
            "phone_no": {"boost": 2},
            "phone_no_alternative": {"boost": 2},
            "sex": {"boost": 1},
            "relationship": {"boost": 1},
            "middle_name": {"boost": 1},
            "admin1": {"boost": 1},
            "admin2": {"boost": 1},
            # household - not used right now
        }
        queries_list = []
        names_queries = cls._prepare_queries_for_names_from_fields(fields)
        documents_queries = cls._prepare_documents_queries_from_fields(fields)
        identities_queries = cls._prepare_identities_queries_from_fields(fields)
        households_and_roles_queries = cls._prepare_households_and_roles_queries_from_fields(fields)
        queries_list.extend(names_queries)
        queries_list.extend(documents_queries)
        queries_list.extend(identities_queries)

        for field_name, field_value in fields.items():
            if field_value is None:
                continue
            if isinstance(field_value, str) and field_value == "":
                continue
            if field_name not in fields_meta.keys():
                continue
            field_meta = fields_meta[field_name]
            queries_to_append = [
                {
                    "match": {
                        field_name: {
                            "query": field_value,
                            "boost": field_meta.get("boost", 1),
                            "operator": field_meta.get("operator", "OR"),
                        }
                    }
                }
            ]
            queries_list.extend(queries_to_append)

        query_dict = {
            "min_score": min_score,
            # TODO add pagination
            "size": "10000",
            "query": {
                "bool": {
                    "minimum_should_match": 1,
                    "should": queries_list,
                    "must_not": [{"match": {"id": {"query": str(individual.id), "boost": 0}}}],
                }
            },
        }
        return query_dict

    @classmethod
    def _prepare_queries_for_names_from_fields(cls, fields):
        given_name = fields.pop("given_name")
        family_name = fields.pop("family_name")
        full_name = fields.pop("full_name")
        if all(x is None for x in (given_name, family_name, full_name)):
            return []
        return cls._prepare_queries_for_names(given_name, family_name, full_name)

    @classmethod
    def _prepare_households_and_roles_queries_from_fields(cls, fields):
        households_and_roles = fields.pop("households_and_roles", [])
        households_and_roles_queries = cls._prepare_households_and_roles_queries(households_and_roles)
        return households_and_roles_queries

    @classmethod
    def _prepare_identities_queries_from_fields(cls, fields):
        identities = fields.pop("identities", [])
        identities_queries = cls._prepare_identities_or_documents_query(identities, "identity")
        return identities_queries

    @classmethod
    def _prepare_documents_queries_from_fields(cls, fields):
        documents = fields.pop("documents", [])
        documents_queries = cls._prepare_identities_or_documents_query(documents, "document")
        return documents_queries

    @staticmethod
    def _prepare_fields(individual, fields_names, dict_fields):
        fields = to_dict(individual, fields=fields_names, dict_fields=dict_fields)
        if not isinstance(fields["phone_no"], str):
            fields["phone_no"] = fields["phone_no"].raw_input
        if not isinstance(fields["phone_no_alternative"], str):
            fields["phone_no_alternative"] = fields["phone_no_alternative"].raw_input

        return fields

    @classmethod
    def _prepare_households_and_roles_queries(cls, households_and_roles):
        """
            Not needed
            Not working
        """
        queries = []
        for item in households_and_roles:
            role = item.get("role")
            individual_id = str(item.get("individual", {}).get("id"))
            if role and individual_id:
                queries.extend(
                    [
                        {
                            "bool": {
                                "must": [
                                    {"match": {"households_and_role.role": {"query": role}}},
                                    {"match": {"households_and_role.individual": {"query": individual_id}}},
                                ],
                                "boost": 2,
                            }
                        }
                    ]
                )

        return queries

    @classmethod
    def _prepare_household_query(cls, household_data):
        queries = []
        important_fields = (
            "address",
            "country",
            "country_origin",
        )
        for key, data in household_data.items():
            if not data or key not in important_fields:
                continue

            if "." in key:
                key = key.split(".")[0]
            if key in ("head_of_household", "id"):
                data = str(data)

            if key in ("admin_area", "admin1", "admin2"):
                if key != "admin_area":
                    admin_areas = {
                        key: data,
                    }
                else:
                    admin_areas = {
                        "admin1": data.title if data else None,
                        "admin2": data.children.filter(admin_area_type__admin_level=2).first(),
                    }
                queries.extend([{"match": {admin_area: {"query": value}}} for admin_area, value in admin_areas.items()])
            else:
                queries.append(
                    {
                        "match": {
                            f"household.{key}": {
                                "query": data.alpha3 if isinstance(data, Country) else data,
                                "boost": 0.4,
                            }
                        }
                    }
                )

        return queries

    @classmethod
    def _prepare_identities_or_documents_query(cls, data, data_type):
        queries = []
        document_type_key = "type"
        prefix = "identities" if data_type.lower() == "identity" else "documents"

        if data_type.lower() == "identity":
            document_type_key = "agency"

        for item in data:
            doc_number = item.get("document_number") or item.get("number")
            doc_type = item.get(document_type_key)
            if doc_number and doc_type:
                queries_list = [
                    {"match": {f"{prefix}.number": {"query": str(doc_number)}}},
                    {"match": {f"{prefix}.{document_type_key}": {"query": doc_type}}},
                ]
                if prefix == "documents":
                    country = item.get("country", "")
                    queries_list.append(
                        {
                            "match": {
                                f"{prefix}.country": {
                                    "query": country.alpha3 if isinstance(country, Country) else country
                                }
                            }
                        },
                    )
                queries.extend(
                    [
                        {
                            "bool": {
                                "must": queries_list,
                                "boost": 4,
                            },
                        }
                    ]
                )

        return queries

    @classmethod
    def _prepare_queries_for_names(cls, given_name, family_name, full_name):
        """
        prepares ES queries for
        * givenName
        * familyName
        or
        * full_name
        max_score 8 if exact match or phonetic exact match
        """
        if not given_name or not family_name:
            # max possible score 7
            return [{"match": {"full_name": {"query": full_name, "boost": 8.0, "operator": "AND"}}}]
        given_name_complex_query = cls._get_complex_query_for_name(given_name, "given_name")
        family_name_complex_query = cls._get_complex_query_for_name(family_name, "family_name")
        names_should_query = {
            "bool": {
                "should": [
                    given_name_complex_query,
                    family_name_complex_query,
                ]
            }
        }
        # max possible score 8
        names_must_query = {
            "bool": {
                "must": [
                    given_name_complex_query,
                    family_name_complex_query,
                ],
                "boost": 4,
            }
        }
        max_from_should_and_must = {"dis_max": {"queries": [names_should_query, names_must_query], "tie_breaker": 0}}

        return [max_from_should_and_must]

    @classmethod
    def _get_complex_query_for_name(cls, name, field_name):
        name_phonetic_query_dict = {"match": {f"{field_name}.phonetic": {"query": name}}}
        # phonetic analyzer not working with fuzziness
        name_fuzzy_query_dict = {
            "match": {
                field_name: {
                    "query": name,
                    "fuzziness": cls.FUZZINESS,
                    "max_expansions": 50,
                    "prefix_length": 0,
                    "fuzzy_transpositions": True,
                }
            }
        }
        # choose max from fuzzy and phonetic
        # phonetic score === 0 or 1
        # fuzzy score <=1 changes if there is need make change
        name_complex_query = {
            "dis_max": {"queries": [name_fuzzy_query_dict, name_phonetic_query_dict], "tie_breaker": 0}
        }
        return name_complex_query

    @classmethod
    def _get_duplicates_tuple(cls, query_dict, duplicate_score, document, individual):
        duplicates = []
        possible_duplicates = []
        original_individuals_ids_duplicates = []
        original_individuals_ids_possible_duplicates = []
        # TODO add pagination
        query = document.search().params(search_type="dfs_query_then_fetch").from_dict(query_dict)
        query._index = document._index._name
        results = query.execute()

        results_data = {
            "duplicates": [],
            "possible_duplicates": [],
        }
        for individual_hit in results:
            score = individual_hit.meta.score
            results_core_data = {
                "hit_id": individual_hit.id,
                "full_name": individual_hit.full_name,
                "score": individual_hit.meta.score,
                "location": individual_hit.admin2,  # + village
                "dob": individual_hit.birth_date,
            }
            if score >= duplicate_score:
                duplicates.append(individual_hit.id)
                original_individuals_ids_duplicates.append(individual.id)
                results_core_data["proximity_to_score"] = score - duplicate_score
                results_data["duplicates"].append(results_core_data)
            elif document == IndividualDocument:
                possible_duplicates.append(individual_hit.id)
                original_individuals_ids_possible_duplicates.append(individual.id)
                results_core_data["proximity_to_score"] = score - config.DEDUPLICATION_GOLDEN_RECORD_MIN_SCORE
                results_data["possible_duplicates"].append(results_core_data)
        log.debug(f"INDIVIDUAL {individual}")
        log.debug([(r.full_name, r.meta.score) for r in results])
        return (
            duplicates,
            possible_duplicates,
            original_individuals_ids_duplicates,
            original_individuals_ids_possible_duplicates,
            results_data,
        )

    @classmethod
    def deduplicate_single_imported_individual(cls, individual):
        fields_names = (
            "given_name",
            "full_name",
            "middle_name",
            "family_name",
            "phone_no",
            "phone_no_alternative",
            "relationship",
            "sex",
            "birth_date",
        )
        dict_fields = {
            "documents": ("document_number", "type.type", "type.country"),
            "identities": ("document_number", "agency.type"),
            "household": (
                "residence_status",
                "country_origin",
                "size",
                "address",
                "country",
                "admin1",
                "admin2",
                "female_age_group_0_5_count",
                "female_age_group_6_11_count",
                "female_age_group_12_17_count",
                "female_age_group_18_59_count",
                "female_age_group_60_count",
                "pregnant_count",
                "male_age_group_0_5_count",
                "male_age_group_6_11_count",
                "male_age_group_12_17_count",
                "male_age_group_18_59_count",
                "male_age_group_60_count",
                "female_age_group_0_5_disabled_count",
                "female_age_group_6_11_disabled_count",
                "female_age_group_12_17_disabled_count",
                "female_age_group_18_59_disabled_count",
                "female_age_group_60_disabled_count",
                "male_age_group_0_5_disabled_count",
                "male_age_group_6_11_disabled_count",
                "male_age_group_12_17_disabled_count",
                "male_age_group_18_59_disabled_count",
                "male_age_group_60_disabled_count",
                "head_of_household.id",
                "returnee",
                "registration_method",
                "collect_individual_data",
                "currency",
                "unhcr_id",
            ),
            "households_and_roles": ("role", "individual.id"),
        }
        fields = cls._prepare_fields(individual, fields_names, dict_fields)

        # query_dict = cls._prepare_query_dict(individual, fields, config.DEDUPLICATION_BATCH_MIN_SCORE, only_in_rdi,)
        query_dict = cls._prepare_query_dict(
            individual,
            fields,
            0,
        )
        # noinspection PyTypeChecker
        query_dict["query"]["bool"]["filter"] = [
            {"term": {"registration_data_import_id": str(individual.registration_data_import.id)}},
        ]
        # print(json.dumps(query_dict, indent=1, cls=DjangoJSONEncoder))
        return cls._get_duplicates_tuple(
            query_dict,
            config.DEDUPLICATION_BATCH_DUPLICATE_SCORE,
            ImportedIndividualDocument,
            individual,
        )

    @classmethod
    def deduplicate_single_individual(cls, individual):
        fields_names = (
            "given_name",
            "full_name",
            "middle_name",
            "family_name",
            "phone_no",
            "phone_no_alternative",
            "relationship",
            "sex",
            "birth_date",
        )
        dict_fields = {
            "documents": ("document_number", "type.type"),
            "identities": ("number", "agency.type"),
            "household": (
                "residence_status",
                "country_origin",
                "size",
                "address",
                "country",
                "admin_area",
                "female_age_group_0_5_count",
                "female_age_group_6_11_count",
                "female_age_group_12_17_count",
                "female_age_group_18_59_count",
                "female_age_group_60_count",
                "pregnant_count",
                "male_age_group_0_5_count",
                "male_age_group_6_11_count",
                "male_age_group_12_17_count",
                "male_age_group_18_59_count",
                "male_age_group_60_count",
                "female_age_group_0_5_disabled_count",
                "female_age_group_6_11_disabled_count",
                "female_age_group_12_17_disabled_count",
                "female_age_group_18_59_disabled_count",
                "female_age_group_60_disabled_count",
                "male_age_group_0_5_disabled_count",
                "male_age_group_6_11_disabled_count",
                "male_age_group_12_17_disabled_count",
                "male_age_group_18_59_disabled_count",
                "male_age_group_60_disabled_count",
                "head_of_household.id",
                "first_registration_date",
                "last_registration_date",
                "returnee",
                "registration_method",
                "collect_individual_data",
                "currency",
                "unhcr_id",
            ),
            "households_and_roles": ("role", "individual.id"),
        }
        fields = cls._prepare_fields(individual, fields_names, dict_fields)

        query_dict = cls._prepare_query_dict(
            individual,
            fields,
            config.DEDUPLICATION_GOLDEN_RECORD_MIN_SCORE,
        )
        query_dict["query"]["bool"]["filter"] = [
            {"term": {"business_area": cls.business_area}},
        ]
        return cls._get_duplicates_tuple(
            query_dict,
            config.DEDUPLICATION_GOLDEN_RECORD_DUPLICATE_SCORE,
            IndividualDocument,
            individual,
        )

    @classmethod
    def _get_duplicated_individuals(cls, registration_data_import, individuals):
        if individuals is None:
            individuals = Individual.objects.filter(registration_data_import=registration_data_import)
        all_duplicates = []
        all_possible_duplicates = []
        all_original_individuals_ids_duplicates = []
        all_original_individuals_ids_possible_duplicates = []
        to_bulk_update_results = []
        for individual in individuals:
            (
                duplicates,
                possible_duplicates,
                original_individuals_ids_duplicates,
                original_individuals_ids_possible_duplicates,
                results_data,
            ) = cls.deduplicate_single_individual(individual)

            individual.deduplication_golden_record_results = results_data
            to_bulk_update_results.append(individual)

            all_duplicates.extend(duplicates)
            all_possible_duplicates.extend(possible_duplicates)
            all_original_individuals_ids_duplicates.extend(original_individuals_ids_duplicates)
            all_original_individuals_ids_possible_duplicates.extend(original_individuals_ids_possible_duplicates)

        return (
            all_duplicates,
            all_possible_duplicates,
            all_original_individuals_ids_duplicates,
            all_original_individuals_ids_possible_duplicates,
            to_bulk_update_results,
        )

    @classmethod
    def deduplicate_individuals(cls, registration_data_import, individuals=None):
        if not registration_data_import:
            cls.business_area = individuals[0].business_area.slug
        else:
            cls.business_area = registration_data_import.business_area.slug
        (
            all_duplicates,
            all_possible_duplicates,
            all_original_individuals_ids_duplicates,
            all_original_individuals_ids_possible_duplicates,
            to_bulk_update_results,
        ) = cls._get_duplicated_individuals(registration_data_import, individuals)
        cls._mark_individuals(
            all_duplicates,
            all_possible_duplicates,
            to_bulk_update_results,
            all_original_individuals_ids_duplicates,
            all_original_individuals_ids_possible_duplicates,
        )

    @classmethod
    def deduplicate_individuals_from_other_source(cls, individuals):
        cls.business_area = individuals[0].business_area.slug
        to_bulk_update_results = []
        for individual in individuals:
            (
                duplicates,
                possible_duplicates,
                original_individuals_ids_duplicates,
                original_individuals_ids_possible_duplicates,
                results_data,
            ) = cls.deduplicate_single_individual(individual)

            individual.deduplication_golden_record_results = results_data
            if duplicates:
                individual.deduplication_golden_record_status = DUPLICATE
            elif possible_duplicates:
                individual.deduplication_golden_record_status = NEEDS_ADJUDICATION

            to_bulk_update_results.append(individual)

        Individual.objects.bulk_update(
            to_bulk_update_results,
            ["deduplication_golden_record_results", "deduplication_golden_record_status"],
        )

    @staticmethod
    def _mark_individuals(
        all_duplicates,
        all_possible_duplicates,
        to_bulk_update_results,
        all_original_individuals_ids_duplicates,
        all_original_individuals_ids_possible_duplicates,
    ):
        Individual.objects.filter(
            id__in=all_possible_duplicates + all_original_individuals_ids_possible_duplicates
        ).update(deduplication_golden_record_status=NEEDS_ADJUDICATION)

        Individual.objects.filter(id__in=all_duplicates + all_original_individuals_ids_duplicates).update(
            deduplication_golden_record_status=DUPLICATE
        )

        Individual.objects.bulk_update(
            to_bulk_update_results,
            ["deduplication_golden_record_results"],
        )

    @staticmethod
    def set_error_message_and_status(registration_data_import, message):
        old_rdi = RegistrationDataImport.objects.get(id=registration_data_import.id)
        registration_data_import.error_message = message
        registration_data_import.status = RegistrationDataImport.DEDUPLICATION_FAILED
        registration_data_import.save()
        log_create(
            RegistrationDataImport.ACTIVITY_LOG_MAPPING, "business_area", None, old_rdi, registration_data_import
        )

    @classmethod
    def deduplicate_imported_individuals(cls, registration_data_import_datahub):
        imported_individuals = ImportedIndividual.objects.filter(
            registration_data_import=registration_data_import_datahub
        )
        populate_index(imported_individuals, ImportedIndividualDocument)

        registration_data_import = RegistrationDataImport.objects.get(id=registration_data_import_datahub.hct_id)
        cls.business_area = registration_data_import_datahub.business_area_slug
        allowed_duplicates_batch_amount = round(
            (imported_individuals.count() or 1) * (config.DEDUPLICATION_BATCH_DUPLICATES_PERCENTAGE / 100)
        )
        allowed_duplicates_golden_record_amount = round(
            (imported_individuals.count() or 1) * (config.DEDUPLICATION_GOLDEN_RECORD_DUPLICATES_PERCENTAGE / 100)
        )

        all_duplicates = []
        all_possible_duplicates = []
        all_original_individuals_ids_duplicates = []
        all_original_individuals_ids_possible_duplicates = []
        to_bulk_update_results = []
        checked_individuals_ids = []
        for imported_individual in imported_individuals:
            (
                imported_individuals_duplicates,
                imported_individuals_possible_duplicates,
                _,
                _,
                results_data_imported,
            ) = cls.deduplicate_single_imported_individual(imported_individual)
            imported_individual.deduplication_batch_results = results_data_imported
            if results_data_imported["duplicates"]:
                imported_individual.deduplication_batch_status = DUPLICATE_IN_BATCH
            else:
                imported_individual.deduplication_batch_status = UNIQUE_IN_BATCH
            all_duplicates.extend(imported_individuals_duplicates)
            all_possible_duplicates.extend(imported_individuals_possible_duplicates)

            (
                _,
                _,
                original_individuals_ids_duplicates,
                original_individuals_ids_possible_duplicates,
                results_data,
            ) = cls.deduplicate_single_individual(imported_individual)
            imported_individual.deduplication_golden_record_results = results_data
            if results_data["duplicates"]:
                imported_individual.deduplication_golden_record_status = DUPLICATE
            elif results_data["possible_duplicates"]:
                imported_individual.deduplication_golden_record_status = NEEDS_ADJUDICATION
            else:
                imported_individual.deduplication_golden_record_status = UNIQUE
            all_original_individuals_ids_duplicates.extend(original_individuals_ids_duplicates)
            all_original_individuals_ids_possible_duplicates.extend(original_individuals_ids_possible_duplicates)

            checked_individuals_ids.append(imported_individual.id)
            to_bulk_update_results.append(imported_individual)

            if len(results_data_imported["duplicates"]) > config.DEDUPLICATION_BATCH_DUPLICATES_ALLOWED:
                message = (
                    "The number of individuals deemed duplicate with an individual record of the batch "
                    f"exceed the maximum allowed ({config.DEDUPLICATION_BATCH_DUPLICATES_ALLOWED})"
                )
                cls.set_error_message_and_status(registration_data_import, message)
                break

            if len(results_data["duplicates"]) > config.DEDUPLICATION_GOLDEN_RECORD_DUPLICATES_ALLOWED:
                message = (
                    "The number of individuals deemed duplicate with an individual record of the batch "
                    f"exceed the maximum allowed ({config.DEDUPLICATION_GOLDEN_RECORD_DUPLICATES_ALLOWED})"
                )
                cls.set_error_message_and_status(registration_data_import, message)
                break

            set_of_all_duplicates = set(all_duplicates)
            set_of_all_original_individuals_ids_duplicates = set(all_original_individuals_ids_duplicates)

            batch_amount_exceeded = (
                len(set_of_all_duplicates) >= allowed_duplicates_batch_amount
            ) and imported_individuals.count() > 1
            golden_record_amount_exceeded = (
                len(set_of_all_original_individuals_ids_duplicates) >= allowed_duplicates_golden_record_amount
            ) and imported_individuals.count() > 1

            checked_individuals_ids.append(imported_individual.id)

            if batch_amount_exceeded:
                message = (
                    f"The percentage of records ({config.DEDUPLICATION_BATCH_DUPLICATES_PERCENTAGE}%), "
                    "deemed as 'duplicate', within a batch has reached the maximum number."
                )
                cls.set_error_message_and_status(registration_data_import, message)
                break
            elif golden_record_amount_exceeded:
                message = (
                    f"The percentage of records ({config.DEDUPLICATION_GOLDEN_RECORD_DUPLICATES_PERCENTAGE}%), "
                    "deemed as 'duplicate', within a population has reached the maximum number."
                )
                cls.set_error_message_and_status(registration_data_import, message)
                break
            elif batch_amount_exceeded and golden_record_amount_exceeded:
                message = (
                    f"The percentage of records (batch: {config.DEDUPLICATION_BATCH_DUPLICATES_PERCENTAGE}%, "
                    f"population: {config.DEDUPLICATION_GOLDEN_RECORD_DUPLICATES_PERCENTAGE}%), "
                    "deemed as 'duplicate', within a batch and population has reached the maximum number."
                )
                cls.set_error_message_and_status(registration_data_import, message)
                break

        ImportedIndividual.objects.bulk_update(
            to_bulk_update_results,
            [
                "deduplication_batch_results",
                "deduplication_golden_record_results",
                "deduplication_batch_status",
                "deduplication_golden_record_status",
            ],
        )
        set_of_all_possible_duplicates = set(all_possible_duplicates)
        set_of_all_duplicates = set(all_duplicates)
        set_of_all_original_individuals_ids_duplicates = set(all_original_individuals_ids_duplicates)
        set_of_all_original_individuals_ids_possible_duplicates = set(all_original_individuals_ids_possible_duplicates)

        registration_data_import_datahub.refresh_from_db()
        if registration_data_import.status == RegistrationDataImport.DEDUPLICATION_FAILED:
            registration_data_import_datahub.individuals.filter(
                Q(deduplication_batch_status=UNIQUE_IN_BATCH) & Q(deduplication_golden_record_status=UNIQUE)
            ).exclude(id__in=checked_individuals_ids).update(
                deduplication_batch_status=NOT_PROCESSED,
                deduplication_golden_record_status=NOT_PROCESSED,
            )
        else:
            registration_data_import_datahub.individuals.exclude(
                Q(id__in=set_of_all_duplicates.union(set_of_all_possible_duplicates))
            ).update(deduplication_batch_status=UNIQUE_IN_BATCH)
            registration_data_import_datahub.individuals.exclude(
                id__in=set_of_all_original_individuals_ids_duplicates.union(
                    set_of_all_original_individuals_ids_possible_duplicates
                )
            ).update(deduplication_golden_record_status=UNIQUE)
            old_rdi = RegistrationDataImport.objects.get(id=registration_data_import.id)
            registration_data_import.status = RegistrationDataImport.IN_REVIEW
            registration_data_import.error_message = ""
            registration_data_import.save()

            log_create(
                RegistrationDataImport.ACTIVITY_LOG_MAPPING, "business_area", None, old_rdi, registration_data_import
            )
