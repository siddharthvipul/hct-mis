from typing import TYPE_CHECKING, Any, Dict, List

from apps.registration_datahub.services.sri_lanka_flex_registration_service import SriLankaRegistrationService
from apps.registration_datahub.services.ukraine_flex_registration_service import (
    UkraineRegistrationService,
    UkraineBaseRegistrationService,
)

if TYPE_CHECKING:
    from uuid import UUID

def get_registration_to_rdi_service_map() -> Dict[int, Any]:
    return {
        2: UkraineBaseRegistrationService,  # ukraine
        3: UkraineBaseRegistrationService,  # ukraine
        11: UkraineRegistrationService, # ukraine
        17: SriLankaRegistrationService,  # sri lanka
        # 18: "czech republic",
        # 19: "czech republic",
    }


def create_task_for_processing_records(service: Any, rdi_id: "UUID", records_ids: List) -> None:
    if celery_task := service.PROCESS_FLEX_RECORDS_TASK:
        celery_task.delay(rdi_id, records_ids)
    # else:
        # TODO: add error msg
