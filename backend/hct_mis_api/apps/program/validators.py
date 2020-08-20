from django.core.exceptions import ValidationError

from core.validators import BaseValidator


class ProgramValidator(BaseValidator):
    @classmethod
    def validate_status_change(cls, *args, **kwargs):
        status_to_set = kwargs.get("program_data").get("status")
        program = kwargs.get("program")
        current_status = program.status
        if status_to_set is None or status_to_set == current_status:
            return
        if current_status == "DRAFT" and status_to_set != "ACTIVE":
            raise ValidationError("Draft status can only be changed to Active")
        elif current_status == "ACTIVE" and status_to_set != "FINISHED":
            raise ValidationError("Active status can only be changed to Finished")
        elif current_status == "FINISHED" and status_to_set != "ACTIVE":
            raise ValidationError("Finished status can only be changed to Active")


class ProgramDeletionValidator(BaseValidator):
    @classmethod
    def validate_is_deletable(cls, program, *args, **kwargs):
        if program.status != "DRAFT":
            raise ValidationError("Only Draft Program can be deleted.")


class CashPlanValidator(BaseValidator):
    pass
