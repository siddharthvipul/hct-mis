# Generated by Django 3.2.19 on 2023-06-10 12:58

import concurrency.fields
from django.conf import settings
import django.contrib.postgres.fields.citext
import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.migrations.operations.special
import django.db.models.deletion
import hct_mis_api.apps.targeting.services.targeting_service
import model_utils.fields
import uuid

def chunk_update(model, callback, fields):
    offset = 0
    chunk_size = 100

    while records := model.objects.all()[offset : offset + chunk_size]:
        offset += chunk_size
        for record in records:
            callback(record)

        model.objects.bulk_update(records, fields)

def assign_approved_by_to_changed_by(apps, schema_editor):
    TargetPopulation = apps.get_model("targeting", "TargetPopulation")

    def rewrite_relation(record):
        record.changed_by = record.approved_by

    chunk_update(TargetPopulation, rewrite_relation, ["changed_by"])

def revert_assign_approved_by_to_changed_by(apps, schema_editor):
    TargetPopulation = apps.get_model("targeting", "TargetPopulation")

    def rewrite_relation(record):
        record.approved_by = record.changed_by

    chunk_update(TargetPopulation, rewrite_relation, ["approved_by"])

def move_from_approved_to_locked(apps, schema_editor):
    TargetPopulation = apps.get_model('targeting', 'TargetPopulation')
    TargetPopulation.objects.filter(status="APPROVED").update(status="LOCKED")

def revert_change_status(apps, schema_editor):
    TargetPopulation = apps.get_model('targeting', 'TargetPopulation')
    TargetPopulation.objects.filter(status="LOCKED").update(status="APPROVED")

def change_tp_statuses(apps, schema_editor):
    TargetPopulation = apps.get_model("targeting", "TargetPopulation")

    for tp in TargetPopulation.objects.filter(status="FINALIZED"):
        tp.status = "READY_FOR_CASH_ASSIST" if tp.sent_to_datahub else "PROCESSING"
        tp.save()


def revert_change_tp_statuses(apps, schema_editor):
    TargetPopulation = apps.get_model("targeting", "TargetPopulation")

    for tp in TargetPopulation.objects.filter(status__in=["PROCESSING", "READY_FOR_CASH_ASSIST"]):
        tp.status = "FINALIZED"
        tp.save()

class Migration(migrations.Migration):

    dependencies = [
        ('steficon', '0002_migration'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('targeting', '0006_migration'),
        ('steficon', '0001_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='targetpopulation',
            name='sent_to_datahub',
            field=models.BooleanField(default=False, help_text='\n            Flag set when TP is processed by airflow task\n            '),
        ),
        migrations.AddField(
            model_name='targetpopulation',
            name='ca_hash_id',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='targetpopulation',
            name='ca_id',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='householdselection',
            name='final',
            field=models.BooleanField(default=True, help_text='\n            When set to True, this means the household has been selected from\n            the candidate list. Only these households will be sent to\n            CashAssist when a sync is run for the associated target population.\n            '),
        ),
        migrations.CreateModel(
            name='TargetingIndividualRuleFilterBlock',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('targeting_criteria_rule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='individuals_filters_blocks', to='targeting.targetingcriteriarule')),
                ('target_only_hoh', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, hct_mis_api.apps.targeting.services.targeting_service.TargetingIndividualRuleFilterBlockBase),
        ),
        migrations.AddField(
            model_name='targetpopulation',
            name='steficon_rule',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='target_populations', to='steficon.rule'),
        ),
        migrations.AddField(
            model_name='targetpopulation',
            name='vulnerability_score_max',
            field=models.DecimalField(decimal_places=3, help_text='Written by a tool such as Corticon.', max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='targetpopulation',
            name='vulnerability_score_min',
            field=models.DecimalField(decimal_places=3, help_text='Written by a tool such as Corticon.', max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='targetpopulation',
            name='version',
            field=concurrency.fields.IntegerVersionField(default=0, help_text='record revision number'),
        ),
        migrations.AlterModelOptions(
            name='targetpopulation',
            options={'verbose_name': 'Target Population'},
        ),
        migrations.AlterField(
            model_name='targetpopulation',
            name='steficon_rule',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='target_populations', to='steficon.rule'),
        ),
        migrations.AlterField(
            model_name='householdselection',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='householdselection',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='targetingcriteria',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='targetingcriteria',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='targetingcriteriarule',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='targetingcriteriarule',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='targetingcriteriarulefilter',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='targetingcriteriarulefilter',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.CreateModel(
            name='TargetingIndividualBlockRuleFilter',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('comparision_method', models.CharField(choices=[('EQUALS', 'Equals'), ('NOT_EQUALS', 'Not Equals'), ('CONTAINS', 'Contains'), ('NOT_CONTAINS', 'Does not contain'), ('RANGE', 'In between <>'), ('NOT_IN_RANGE', 'Not in between <>'), ('GREATER_THAN', 'Greater than'), ('LESS_THAN', 'Less than')], max_length=20)),
                ('is_flex_field', models.BooleanField(default=False)),
                ('field_name', models.CharField(max_length=50)),
                ('arguments', django.contrib.postgres.fields.jsonb.JSONField(help_text='\n            Array of arguments\n            ')),
                ('individuals_filters_block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='individual_block_filters', to='targeting.targetingindividualrulefilterblock')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, hct_mis_api.apps.targeting.services.targeting_service.TargetingCriteriaFilterBase),
        ),
        migrations.AlterField(
            model_name='targetpopulation',
            name='ca_hash_id',
            field=django.contrib.postgres.fields.citext.CICharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='targetpopulation',
            name='ca_id',
            field=django.contrib.postgres.fields.citext.CICharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='targetpopulation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='targetpopulation',
            name='name',
            field=django.contrib.postgres.fields.citext.CICharField(db_index=True, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='targetpopulation',
            name='sent_to_datahub',
            field=models.BooleanField(db_index=True, default=False, help_text='\n            Flag set when TP is processed by airflow task\n            '),
        ),
        migrations.AlterField(
            model_name='targetpopulation',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'Open'), ('APPROVED', 'Closed'), ('FINALIZED', 'Sent')], db_index=True, default='DRAFT', max_length=256),
        ),
        migrations.AlterField(
            model_name='targetpopulation',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='targetpopulation',
            name='approved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_target_populations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='targetpopulation',
            name='ca_hash_id',
            field=django.contrib.postgres.fields.citext.CICharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='targetpopulation',
            name='ca_id',
            field=django.contrib.postgres.fields.citext.CICharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='targetpopulation',
            name='finalized_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='targetpopulation',
            name='finalized_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='finalized_target_populations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='targetpopulation',
            name='name',
            field=django.contrib.postgres.fields.citext.CICharField(db_index=True, max_length=255, unique=True, validators=[django.core.validators.MinLengthValidator(3), django.core.validators.MaxLengthValidator(255), django.core.validators.RegexValidator('\\s{2,}', 'Double spaces characters are not allowed.', code='double_spaces_characters_not_allowed', inverse_match=True), django.core.validators.RegexValidator('(^\\s+)|(\\s+$)', 'Leading or trailing spaces characters are not allowed.', code='leading_trailing_spaces_characters_not_allowed', inverse_match=True), django.core.validators.ProhibitNullCharactersValidator()]),
        ),
        migrations.AlterField(
            model_name='targetpopulation',
            name='steficon_rule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='target_populations', to='steficon.rule'),
        ),
        migrations.AlterField(
            model_name='targetpopulation',
            name='vulnerability_score_max',
            field=models.DecimalField(blank=True, decimal_places=3, help_text='Written by a tool such as Corticon.', max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='targetpopulation',
            name='vulnerability_score_min',
            field=models.DecimalField(blank=True, decimal_places=3, help_text='Written by a tool such as Corticon.', max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='targetpopulation',
            name='sent_to_datahub',
            field=models.BooleanField(db_index=True, default=False, help_text='\n            Flag set when TP is processed by celery task\n            '),
        ),
        migrations.AddField(
            model_name='targetpopulation',
            name='excluded_ids',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='targetpopulation',
            name='exclusion_reason',
            field=models.TextField(blank=True),
        ),
        migrations.RenameField(
            model_name='targetpopulation',
            old_name='approved_at',
            new_name='change_date',
        ),
        migrations.AlterField(
            model_name='targetpopulation',
            name='change_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='targetpopulation',
            name='changed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='locked_target_populations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RunPython(assign_approved_by_to_changed_by, revert_assign_approved_by_to_changed_by),
        migrations.RemoveField(
            model_name='targetpopulation',
            name='approved_by',
        ),
        migrations.AlterField(
            model_name='targetpopulation',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'Open'), ('LOCKED', 'Locked'), ('FINALIZED', 'Sent')], db_index=True, default='DRAFT', max_length=256),
        ),
        migrations.RunPython(move_from_approved_to_locked, revert_change_status),
        migrations.AddField(
            model_name='targetpopulation',
            name='steficon_applied_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='targetpopulation',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'Open'), ('LOCKED', 'Locked'), ('PROCESSING', 'Processing'), ('READY_FOR_CASH_ASSIST', 'Ready for cash assist')], db_index=True, default='DRAFT', max_length=256),
        ),
        migrations.RunPython(change_tp_statuses, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='targetpopulation',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'Open'), ('LOCKED', 'Locked'), ('STEFICON_WAIT', 'Waiting for Rule Engine'), ('STEFICON_RUN', 'Rule Engine Running'), ('STEFICON_COMPLETED', 'Rule Engine Completed'), ('STEFICON_ERROR', 'Rule Engine Errored'), ('PROCESSING', 'Processing'), ('READY_FOR_CASH_ASSIST', 'Ready for cash assist')], db_index=True, default='DRAFT', max_length=256),
        ),
    ]
