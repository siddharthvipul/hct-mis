import csv
import logging
import os
import tempfile
from datetime import datetime
from functools import wraps

from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from hct_mis_api.apps.core.celery import app
from hct_mis_api.apps.core.models import StorageFile, XLSXKoboTemplate
from hct_mis_api.apps.core.tasks.upload_new_template_and_update_flex_fields import (
    KoboRetriableError,
)
from hct_mis_api.apps.household.models import (
    COLLECT_TYPE_NONE,
    IDENTIFICATION_TYPE_NATIONAL_PASSPORT,
    IDENTIFICATION_TYPE_TAX_ID,
    MALE,
    BankAccountInfo,
    Document,
    DocumentType,
    Household,
    Individual,
)
from hct_mis_api.apps.program.models import Program
from hct_mis_api.apps.registration_data.models import RegistrationDataImport
from hct_mis_api.apps.targeting.models import TargetPopulation
from hct_mis_api.apps.utils.logs import log_start_and_end
from hct_mis_api.apps.utils.sentry import sentry_tags

logger = logging.getLogger(__name__)


class transaction_celery_task:  # used as decorator
    def __init__(self, *args, **kwargs):
        self.task_args = args
        self.task_kwargs = kwargs

    def __call__(self, func):
        @wraps(func)
        def wrapper_func(*args, **kwargs):
            try:
                with transaction.atomic():
                    return func(*args, **kwargs)
            except Exception as e:
                logger.error(e)

        task_func = app.task(*self.task_args, **self.task_kwargs)(wrapper_func)
        return task_func


@app.task(bind=True, default_retry_delay=60)
@log_start_and_end
@sentry_tags
def upload_new_kobo_template_and_update_flex_fields_task_with_retry(self, xlsx_kobo_template_id):
    try:
        from hct_mis_api.apps.core.tasks.upload_new_template_and_update_flex_fields import (
            UploadNewKoboTemplateAndUpdateFlexFieldsTask,
        )

        UploadNewKoboTemplateAndUpdateFlexFieldsTask().execute(xlsx_kobo_template_id=xlsx_kobo_template_id)
    except KoboRetriableError as exc:
        from datetime import timedelta

        from django.utils import timezone

        one_day_earlier_time = timezone.now() - timedelta(days=1)
        if exc.xlsx_kobo_template_object.first_connection_failed_time > one_day_earlier_time:
            logger.exception(exc)
            raise self.retry(exc=exc)
        else:
            exc.xlsx_kobo_template_object.status = XLSXKoboTemplate.UNSUCCESSFUL
    except Exception as e:
        logger.exception(e)
        raise


@app.task
@log_start_and_end
@sentry_tags
def upload_new_kobo_template_and_update_flex_fields_task(xlsx_kobo_template_id):
    try:
        from hct_mis_api.apps.core.tasks.upload_new_template_and_update_flex_fields import (
            UploadNewKoboTemplateAndUpdateFlexFieldsTask,
        )

        UploadNewKoboTemplateAndUpdateFlexFieldsTask().execute(xlsx_kobo_template_id=xlsx_kobo_template_id)
    except KoboRetriableError:
        upload_new_kobo_template_and_update_flex_fields_task_with_retry.delay(xlsx_kobo_template_id)
    except Exception as e:
        logger.exception(e)
        raise


@app.task
@sentry_tags
def create_target_population_task(storage_id, rdi_name):
    storage_obj = StorageFile.objects.get(id=storage_id)
    file_path = None
    try:
        with transaction.atomic(), transaction.atomic("registration_datahub"):

            business_area = storage_obj.business_area

            passport_type = DocumentType.objects.get(
                Q(country=business_area.countries.first()) & Q(type=IDENTIFICATION_TYPE_NATIONAL_PASSPORT)
            )
            tax_type = DocumentType.objects.get(
                Q(country=business_area.countries.first()) & Q(type=IDENTIFICATION_TYPE_TAX_ID)
            )

            first_registration_date = datetime.now()
            last_registration_date = first_registration_date

            family_ids = set()
            individuals, documents, bank_infos = [], [], []

            storage_obj.status = StorageFile.STATUS_PROCESSING
            storage_obj.save(update_fields=["status"])
            rows_count = 0

            # TODO fix to use Azure storage override AzureStorageFile open method
            with storage_obj.file.open("rb") as original_file, tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(original_file.read())
                file_path = tmp.name

            with open(file_path, encoding="cp1251") as file:
                reader = csv.DictReader(file, delimiter=";")
                batch_size = 10000
                current_batch_index = 0
                registration_data_import = None
                for row in reader:
                    rows_count += 1
                    family_id = row["ID_FAM"]
                    iban = row["IBAN"]
                    tax_id = row["N_ID"]
                    passport_id = row["PASSPORT"]
                    size = row["FAM_NUM"]
                    if current_batch_index % batch_size == 0:
                        registration_data_import = RegistrationDataImport.objects.create(
                            name=f"{rdi_name} part {int(current_batch_index//batch_size)+1}",
                            number_of_individuals=0,
                            number_of_households=0,
                            business_area=storage_obj.business_area,
                            data_source=RegistrationDataImport.EDOPOMOGA,
                        )
                    current_batch_index += 1

                    individual_data = {
                        "given_name": row.get("NAME", ""),
                        "middle_name": row.get("PATRONYMIC", ""),
                        "family_name": row.get("SURNAME", ""),
                        "full_name": f'{row.get("NAME", "")} {row.get("PATRONYMIC", "")} {row.get("SURNAME", "")}',
                        "birth_date": datetime.strptime(row["BDATE"], "%d.%m.%Y").date(),
                        "phone_no": row.get("PHONЕ", ""),
                        "business_area": business_area,
                        "first_registration_date": first_registration_date,
                        "last_registration_date": last_registration_date,
                        "sex": MALE,
                    }
                    if family_id in family_ids:
                        individual = Individual(**individual_data, household=Household.objects.get(family_id=family_id))
                        individuals.append(individual)
                    else:
                        individual = Individual.objects.create(**individual_data)
                        individual.refresh_from_db()

                        household = Household.objects.create(
                            head_of_household=individual,
                            business_area=business_area,
                            first_registration_date=first_registration_date,
                            last_registration_date=last_registration_date,
                            registration_data_import=registration_data_import,
                            size=size,
                            family_id=family_id,
                            storage_obj=storage_obj,
                            collect_individual_data=COLLECT_TYPE_NONE,
                        )

                        individual.household = household
                        individual.save()

                        family_ids.add(family_id)

                    passport = Document(
                        document_number=passport_id,
                        type=passport_type,
                        individual=individual,
                        status=Document.STATUS_INVALID,
                    )

                    tax = Document(
                        document_number=tax_id, type=tax_type, individual=individual, status=Document.STATUS_INVALID
                    )

                    bank_account_info = BankAccountInfo(bank_account_number=iban, individual=individual)

                    documents.append(passport)
                    documents.append(tax)
                    bank_infos.append(bank_account_info)
                    # TODO refactor chunking
                    if rows_count % 1000 == 0:
                        Individual.objects.bulk_create(individuals)
                        Document.objects.bulk_create(documents)
                        BankAccountInfo.objects.bulk_create(bank_infos)
                        individuals = []
                        documents = []
                        bank_infos = []

            Individual.objects.bulk_create(individuals)
            Document.objects.bulk_create(documents)
            BankAccountInfo.objects.bulk_create(bank_infos)

            storage_obj.status = StorageFile.STATUS_FINISHED
            storage_obj.save(update_fields=["status"])
    except Exception:
        storage_obj.status = StorageFile.STATUS_FAILED
        storage_obj.save(update_fields=["status"])
        raise
    finally:
        if file_path:
            os.remove(file_path)
