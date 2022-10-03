from django.contrib.auth import get_user_model
from hct_mis_api.apps.program.models import Program
from hct_mis_api.apps.core.utils import decode_id_string
from hct_mis_api.apps.accountability.models import Feedback
from hct_mis_api.apps.core.models import BusinessArea
from hct_mis_api.apps.household.models import Household, Individual
from hct_mis_api.apps.geo.models import Area
from django.shortcuts import get_object_or_404

User = get_user_model()


class FeedbackCrudServices:
    @classmethod
    def validate_lookup(cls, feedback):
        # pass
        if feedback.household_lookup is not None and feedback.individual_lookup is not None:
            if feedback.household_lookup != feedback.individual_lookup.household:
                raise Exception("Household lookup does not match individual lookup")

    @classmethod
    def create(cls, user: User, input_data: dict) -> Feedback:
        obj = Feedback(
            business_area=BusinessArea.objects.get(slug=input_data["business_area_slug"]),
            issue_type=input_data["issue_type"],
            description=input_data["description"],
        )
        if input_data.get("household_lookup"):
            obj.household_lookup = get_object_or_404(Household, id=decode_id_string(input_data["household_lookup"]))
        if input_data.get("individual_lookup"):
            obj.individual_lookup = get_object_or_404(Individual, id=decode_id_string(input_data["individual_lookup"]))
        if input_data.get("comments"):
            obj.comments = input_data["comments"]
        if input_data.get("admin2"):
            obj.admin2 = get_object_or_404(Area, id=decode_id_string(input_data["admin2"]))
        if input_data.get("area"):
            obj.area = input_data["area"]
        if input_data.get("language"):
            obj.language = input_data["language"]
        if input_data.get("consent"):
            obj.consent = input_data["consent"]
        if input_data.get("program"):
            obj.program = get_object_or_404(Program, id=decode_id_string(input_data["program"]))
        obj.created_by = user
        cls.validate_lookup(obj)
        obj.save()
        return obj

    @classmethod
    def update(cls, feedback: Feedback, input_data: dict) -> Feedback:
        if "issue_type" in input_data:
            feedback.issue_type = input_data["issue_type"]
        if "description" in input_data:
            feedback.description = input_data["description"]
        if "household_lookup" in input_data:
            feedback.household_lookup = get_object_or_404(
                Household, id=decode_id_string(input_data["household_lookup"])
            )
        if "individual_lookup" in input_data:
            feedback.individual_lookup = get_object_or_404(
                Individual, id=decode_id_string(input_data["individual_lookup"])
            )
        if "comments" in input_data:
            feedback.comments = input_data["comments"]
        if "admin2" in input_data:
            feedback.admin2 = get_object_or_404(Area, id=decode_id_string(input_data["admin2"]))
        if "area" in input_data:
            feedback.area = input_data["area"]
        if "language" in input_data:
            feedback.language = input_data["language"]
        if "consent" in input_data:
            feedback.consent = input_data["consent"]
        if "program" in input_data:
            feedback.program = get_object_or_404(Program, id=decode_id_string(input_data["program"]))
        cls.validate_lookup(feedback)
        feedback.save()
        return feedback
