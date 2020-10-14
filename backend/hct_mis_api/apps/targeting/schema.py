import django_filters
import graphene
from django.db.models import Q, Prefetch
from django_filters import FilterSet, CharFilter
from graphene import relay, Scalar
from graphene_django import DjangoObjectType, DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField

import targeting.models as target_models
from core.core_fields_attributes import CORE_FIELDS_ATTRIBUTES_DICTIONARY
from core.filters import IntegerFilter
from core.models import FlexibleAttribute
from core.schema import ExtendedConnection, FieldAttributeNode, ChoiceObject
from core.utils import decode_id_string
from household.models import Household
from household.schema import HouseholdNode
from targeting.validators import TargetingCriteriaInputValidator


class HouseholdFilter(FilterSet):
    order_by = django_filters.OrderingFilter(
        fields=(
            "id",
            "head_of_household__full_name",
            "size",
            "admin_area__title",
            "updated_at",
        )
    )


class TargetPopulationFilter(django_filters.FilterSet):
    """Query target population records.

    Loads associated entries for Households and TargetRules.
    """

    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    created_by_name = django_filters.CharFilter(field_name="created_by", method="filter_created_by_name")
    candidate_list_total_households_min = IntegerFilter(
        field_name="candidate_list_total_households",
        lookup_expr="gte",
    )
    candidate_list_total_households_max = IntegerFilter(
        field_name="candidate_list_total_households",
        lookup_expr="lte",
    )
    candidate_list_total_individuals_min = IntegerFilter(
        field_name="candidate_list_total_individuals",
        lookup_expr="gte",
    )
    candidate_list_total_individuals_max = IntegerFilter(
        field_name="candidate_list_total_individuals",
        lookup_expr="lte",
    )

    final_list_total_households_min = IntegerFilter(
        field_name="final_list_total_households",
        lookup_expr="gte",
    )
    final_list_total_households_max = IntegerFilter(
        field_name="final_list_total_households",
        lookup_expr="lte",
    )
    final_list_total_individuals_min = IntegerFilter(
        field_name="final_list_total_individuals",
        lookup_expr="gte",
    )
    final_list_total_individuals_max = IntegerFilter(
        field_name="final_list_total_individuals",
        lookup_expr="lte",
    )
    business_area = CharFilter(field_name="business_area__slug")

    @staticmethod
    def filter_created_by_name(queryset, model_field, value):
        """Gets full name of the associated user from query."""
        fname_query_key = f"{model_field}__given_name__icontains"
        lname_query_key = f"{model_field}__family_name__icontains"
        for name in value.strip().split():
            queryset = queryset.filter(Q(**{fname_query_key: name}) | Q(**{lname_query_key: name}))
        return queryset

    class Meta:
        model = target_models.TargetPopulation
        fields = (
            "name",
            "created_by_name",
            "created_at",
            "updated_at",
            "status",
            "households",
        )

        filter_overrides = {
            target_models.IntegerRangeField: {"filter_class": django_filters.NumericRangeFilter},
            target_models.models.DateTimeField: {"filter_class": django_filters.DateTimeFilter},
        }

    order_by = django_filters.OrderingFilter(
        fields=(
            "name",
            "created_at",
            "created_by",
            "updated_at",
            "status",
            "total_households",
            "total_family_size",
        )
    )


class Arg(Scalar):
    """
    Allows use of a JSON String for input / output from the GraphQL schema.

    Use of this type is *not recommended* as you lose the benefits of having a defined, static
    schema (one of the key benefits of GraphQL).
    """

    @staticmethod
    def serialize(dt):
        return dt

    @staticmethod
    def parse_literal(node):
        return node

    @staticmethod
    def parse_value(value):
        return value


class TargetingCriteriaRuleFilterNode(DjangoObjectType):
    arguments = graphene.List(Arg)
    field_attribute = graphene.Field(FieldAttributeNode)

    def resolve_arguments(self, info):
        return self.arguments

    def resolve_field_attribute(parent, info):
        if parent.is_flex_field:
            return FlexibleAttribute.objects.get(name=parent.field_name)
        else:
            return CORE_FIELDS_ATTRIBUTES_DICTIONARY.get(parent.field_name)

    class Meta:
        model = target_models.TargetingCriteriaRuleFilter


class TargetingCriteriaRuleNode(DjangoObjectType):
    filters = graphene.List(TargetingCriteriaRuleFilterNode)

    def resolve_filters(self, info):
        return self.filters.all()

    class Meta:
        model = target_models.TargetingCriteriaRule


class TargetingCriteriaNode(DjangoObjectType):
    rules = graphene.List(TargetingCriteriaRuleNode)

    def resolve_rules(self, info):
        return self.rules.all()

    class Meta:
        model = target_models.TargetingCriteria


class StatsObjectType(graphene.ObjectType):
    child_male = graphene.Int()
    child_female = graphene.Int()
    adult_male = graphene.Int()
    adult_female = graphene.Int()


class TargetPopulationNode(DjangoObjectType):
    """Defines an individual target population record."""

    total_households = graphene.Int(source="total_households")
    total_family_size = graphene.Int(source="total_family_size")
    candidate_list_targeting_criteria = TargetingCriteriaRuleFilterNode()
    final_list_targeting_criteria = TargetingCriteriaRuleFilterNode()
    final_list = DjangoConnectionField(HouseholdNode)
    candidate_stats = graphene.Field(StatsObjectType)
    final_stats = graphene.Field(StatsObjectType)

    class Meta:
        model = target_models.TargetPopulation
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection
        filterset_class = TargetPopulationFilter


class TargetingCriteriaRuleFilterObjectType(graphene.InputObjectType):
    comparision_method = graphene.String(required=True)
    is_flex_field = graphene.Boolean(required=True)
    field_name = graphene.String(required=True)
    arguments = graphene.List(Arg, required=True)


class TargetingIndividualRuleFilterBlockObjectType(graphene.InputObjectType):
    individual_block_filters = graphene.List(TargetingCriteriaRuleFilterObjectType)


class TargetingCriteriaRuleObjectType(graphene.InputObjectType):
    filters = graphene.List(TargetingCriteriaRuleFilterObjectType)
    individuals_filters_blocks = graphene.List(TargetingIndividualRuleFilterBlockObjectType)


class TargetingCriteriaObjectType(graphene.InputObjectType):
    rules = graphene.List(TargetingCriteriaRuleObjectType)


def targeting_criteria_object_type_to_query(targeting_criteria_object_type):
    TargetingCriteriaInputValidator.validate(targeting_criteria_object_type)
    targeting_criteria_querying = target_models.TargetingCriteriaQueryingMixin([])
    for rule in targeting_criteria_object_type.get("rules", []):
        targeting_criteria_rule_querying = target_models.TargetingCriteriaRuleQueryingMixin(
            filters=[], individuals_filters_blocks=[]
        )
        for filter_dict in rule.get("filters", []):
            targeting_criteria_rule_querying.filters.append(target_models.TargetingCriteriaRuleFilter(**filter_dict))
        for individuals_filters_block_dict in rule.get("filters", []):
            individuals_filters_block = target_models.TargetingIndividualRuleFilterBlockMixin([])
            targeting_criteria_rule_querying.individuals_filters_blocks.append(individuals_filters_block)
            for individual_block_filter_dict in individuals_filters_block_dict.get("individual_block_filters", []):
                individuals_filters_block.individual_block_filters.append(
                    target_models.TargetingIndividualBlockRuleFilter(**individual_block_filter_dict)
                )
        targeting_criteria_querying.rules.append(targeting_criteria_rule_querying)
    return targeting_criteria_querying.get_query()


def prefetch_selections(qs, target_population=None):
    return qs.prefetch_related(
        Prefetch(
            "selections",
            queryset=target_models.HouseholdSelection.objects.filter(target_population=target_population),
        )
    )


class Query(graphene.ObjectType):
    target_population = relay.Node.Field(TargetPopulationNode)
    all_target_population = DjangoFilterConnectionField(TargetPopulationNode)
    golden_record_by_targeting_criteria = DjangoFilterConnectionField(
        HouseholdNode,
        targeting_criteria=TargetingCriteriaObjectType(required=True),
        filterset_class=HouseholdFilter,
    )
    candidate_households_list_by_targeting_criteria = DjangoFilterConnectionField(
        HouseholdNode,
        target_population=graphene.Argument(graphene.ID, required=True),
        filterset_class=HouseholdFilter,
    )
    final_households_list_by_targeting_criteria = DjangoFilterConnectionField(
        HouseholdNode,
        target_population=graphene.Argument(graphene.ID, required=True),
        targeting_criteria=TargetingCriteriaObjectType(),
        filterset_class=HouseholdFilter,
    )
    target_population_status_choices = graphene.List(ChoiceObject)

    def resolve_target_population_status_choices(self, info, **kwargs):
        return [{"name": name, "value": value} for value, name in target_models.TargetPopulation.STATUS_CHOICES]

    def resolve_candidate_households_list_by_targeting_criteria(parent, info, target_population, **kwargs):
        target_population_id = decode_id_string(target_population)
        target_population_model = target_models.TargetPopulation.objects.get(pk=target_population_id)
        if target_population_model.status == "DRAFT":
            return prefetch_selections(
                Household.objects.filter(target_population_model.candidate_list_targeting_criteria.get_query()),
            ).distinct()
        return prefetch_selections(target_population_model.households, target_population_model).all()

    def resolve_final_households_list_by_targeting_criteria(
        parent, info, target_population, targeting_criteria=None, **kwargs
    ):
        target_population_id = decode_id_string(target_population)
        target_population_model = target_models.TargetPopulation.objects.get(pk=target_population_id)
        if target_population_model.status == "DRAFT":
            return []
        if target_population_model.status == "APPROVED":
            if targeting_criteria is None:
                if target_population_model.final_list_targeting_criteria:
                    return (
                        prefetch_selections(
                            target_population_model.households.filter(
                                target_population_model.final_list_targeting_criteria.get_query()
                            ),
                            target_population_model,
                        )
                        .order_by("created_at")
                        .distinct()
                    )
                else:
                    return (
                        prefetch_selections(
                            target_population_model.households,
                            target_population_model,
                        )
                        .order_by("created_at")
                        .all()
                    )
            return (
                prefetch_selections(
                    target_population_model.households.filter(
                        targeting_criteria_object_type_to_query(targeting_criteria)
                    ),
                    target_population_model,
                )
                .order_by("created_at")
                .all()
                .distinct()
            )
        return (
            target_population_model.final_list.order_by("created_at")
            .prefetch_related(
                Prefetch(
                    "selections",
                    queryset=target_models.HouseholdSelection.objects.filter(target_population=target_population_model),
                )
            )
            .all()
        )

    def resolve_golden_record_by_targeting_criteria(parent, info, targeting_criteria, **kwargs):
        return prefetch_selections(
            Household.objects.filter(targeting_criteria_object_type_to_query(targeting_criteria))
        ).distinct()
