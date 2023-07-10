# Generated by Django 3.2.19 on 2023-06-08 19:37

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.migrations.operations.special
import django.db.models.deletion
import model_utils.fields
import uuid

from django.core.paginator import Paginator


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
def empty_reverse(apps, schema_editor):
    pass


def move_status_to_summary(apps, schema_editor):
    CashPlan = apps.get_model("program", "CashPlan")
    CashPlanPaymentVerificationSummary = apps.get_model("payment", "CashPlanPaymentVerificationSummary")
    for cash_plan in CashPlan.objects.all():
        verification = cash_plan.verifications.first()
        activation_date = None
        completion_date = None
        if verification:
            activation_date = verification.activation_date
            completion_date = verification.completion_date
        CashPlanPaymentVerificationSummary.objects.create(
            status=cash_plan.verification_status,
            cash_plan=cash_plan,
            activation_date=activation_date,
            completion_date=completion_date,
        )


def migrate_data(apps, schema_editor):
    PaymentVerification = apps.get_model('payment', 'PaymentVerification')

    payment_verifications = PaymentVerification.objects.all().order_by("-id")
    paginator = Paginator(payment_verifications, 100)
    for page in paginator.page_range:
        for payment_verification in paginator.page(page).object_list:
            payment_verification.payment_record_new = payment_verification.payment_record
            payment_verification.save()

def get_cash_plan_payment_verification_model(apps):
    return apps.get_model("payment", "CashPlanPaymentVerification")


class Migrator:
    uuids = []

    @staticmethod
    def save_current_uuids(apps, schema_editor):
        for cppv in get_cash_plan_payment_verification_model(apps).objects.all():
            if cppv.rapid_pro_flow_start_uuid:
                Migrator.uuids.append({"cppv": cppv.pk, "uuid": cppv.rapid_pro_flow_start_uuid})

    @staticmethod
    def apply_saved_uuids(apps, schema_editor):
        for uuid in Migrator.uuids:
            cppv = get_cash_plan_payment_verification_model(apps).objects.get(pk=uuid["cppv"])
            cppv.rapid_pro_flow_start_uuids = [uuid["uuid"]]
            cppv.save()

class Migration(migrations.Migration):

    dependencies = [
        ('program', '0030_migration'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0010_migration_squashed_0029_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceprovider',
            name='full_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='serviceprovider',
            name='short_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='serviceprovider',
            name='vision_id',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='cashplanpaymentverification',
            name='unicef_id',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.RunSQL(
            sql='ALTER TABLE payment_cashplanpaymentverification ADD unicef_id_index SERIAL',
        ),
        migrations.RunSQL(
            sql="\n        CREATE OR REPLACE FUNCTION create_pvp_unicef_id() RETURNS trigger\n            LANGUAGE plpgsql\n            AS $$\n        BEGIN\n            NEW.unicef_id := format('PVP-%s', NEW.unicef_id_index);\n            return NEW;\n        END\n        $$;\n        \n        CREATE TRIGGER create_pvp_unicef_id BEFORE INSERT ON payment_cashplanpaymentverification FOR EACH ROW EXECUTE PROCEDURE create_pvp_unicef_id();\n        ",
        ),
        migrations.RunSQL(
            sql="UPDATE payment_cashplanpaymentverification SET unicef_id = format('PVP-%s', unicef_id_index)",
        ),
        migrations.AddField(
            model_name='paymentrecord',
            name='is_included',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='paymentrecord',
            name='status',
            field=models.CharField(choices=[('Distribution Successful', 'Distribution Successful'), ('Not Distributed', 'Not Distributed'), ('Transaction Successful', 'Transaction Successful'), ('Transaction Erroneous', 'Transaction Erroneous')], max_length=255),
        ),
        migrations.CreateModel(
            name='CashPlanPaymentVerificationSummary',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('ACTIVE', 'Active'), ('FINISHED', 'Finished')], db_index=True, default='PENDING', max_length=50)),
                ('activation_date', models.DateTimeField(null=True)),
                ('completion_date', models.DateTimeField(null=True)),
                ('cash_plan', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cash_plan_payment_verification_summary', to='program.cashplan')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RunPython(move_status_to_summary, empty_reverse),
        migrations.AddField(
            model_name='paymentverification',
            name='payment_record_new',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='verification', to='payment.paymentrecord'),
        ),
        migrations.RunPython(migrate_data, migrations.RunPython.noop),
        migrations.RenameField(
            model_name='paymentverification',
            old_name='payment_record',
            new_name='payment_record_old',
        ),
        migrations.RenameField(
            model_name='paymentverification',
            old_name='payment_record_new',
            new_name='payment_record',
        ),
        migrations.RemoveField(
            model_name='paymentverification',
            name='payment_record_old',
        ),
        migrations.RemoveField(
            model_name='paymentrecord',
            name='is_included',
        ),
        migrations.RenameField(
            model_name='cashplanpaymentverification',
            old_name='verification_method',
            new_name='verification_channel',
        ),
        migrations.AlterModelOptions(
            name='cashplanpaymentverification',
            options={'ordering': ('created_at',)},
        ),
        migrations.AlterField(
            model_name='cashplanpaymentverification',
            name='age_filter',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='cashplanpaymentverification',
            name='excluded_admin_areas_filter',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='cashplanpaymentverificationsummary',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('ACTIVE', 'Active'), ('FINISHED', 'Finished')], db_index=True, default='PENDING', max_length=50, verbose_name='Verification status'),
        ),
        migrations.AlterField(
            model_name='cashplanpaymentverification',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'Active'), ('FINISHED', 'Finished'), ('PENDING', 'Pending')], db_index=True, default='PENDING', max_length=50),
        ),
        migrations.AlterField(
            model_name='cashplanpaymentverification',
            name='verification_channel',
            field=models.CharField(choices=[('MANUAL', 'MANUAL'), ('RAPIDPRO', 'RAPIDPRO'), ('XLSX', 'XLSX')], max_length=50),
        ),
        migrations.AlterField(
            model_name='cashplanpaymentverificationsummary',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'Active'), ('FINISHED', 'Finished'), ('PENDING', 'Pending')], db_index=True, default='PENDING', max_length=50, verbose_name='Verification status'),
        ),
        migrations.AlterField(
            model_name='paymentverification',
            name='status',
            field=models.CharField(choices=[('NOT_RECEIVED', 'NOT RECEIVED'), ('PENDING', 'PENDING'), ('RECEIVED', 'RECEIVED'), ('RECEIVED_WITH_ISSUES', 'RECEIVED WITH ISSUES')], default='PENDING', max_length=50),
        ),
        migrations.RunPython(Migrator.save_current_uuids, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='cashplanpaymentverification',
            name='rapid_pro_flow_start_uuid',
        ),
        migrations.AddField(
            model_name='cashplanpaymentverification',
            name='rapid_pro_flow_start_uuids',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255), default=list, size=None),
            preserve_default=False,
        ),
        migrations.RunPython(Migrator.apply_saved_uuids, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='cashplanpaymentverification',
            name='rapid_pro_flow_start_uuids',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255), default=list, size=None),
        ),
        migrations.AlterField(
            model_name='cashplanpaymentverification',
            name='unicef_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='cashplanpaymentverification',
            name='xlsx_file_exporting',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cashplanpaymentverification',
            name='xlsx_file_imported',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='cashplanpaymentverification',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'Active'), ('FINISHED', 'Finished'), ('PENDING', 'Pending'), ('INVALID', 'Invalid')], db_index=True, default='PENDING', max_length=50),
        ),
        migrations.CreateModel(
            name='XlsxCashPlanPaymentVerificationFile',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('file', models.FileField(upload_to='')),
                ('was_downloaded', models.BooleanField(default=False)),
                ('cash_plan_payment_verification', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='xlsx_cashplan_payment_verification_file', to='payment.cashplanpaymentverification')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='paymentrecord',
            name='status',
            field=models.CharField(choices=[('Distribution Successful', 'Distribution Successful'), ('Not Distributed', 'Not Distributed'), ('Transaction Successful', 'Transaction Successful'), ('Transaction Erroneous', 'Transaction Erroneous'), ('Force failed', 'Force failed')], max_length=255),
        ),
        migrations.AddField(
            model_name='cashplanpaymentverification',
            name='error',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='paymentverification',
            name='sent_to_rapid_pro',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='cashplanpaymentverification',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'Active'), ('FINISHED', 'Finished'), ('PENDING', 'Pending'), ('INVALID', 'Invalid'), ('RAPID_PRO_ERROR', 'RapidPro Error')], db_index=True, default='PENDING', max_length=50),
        ),
        migrations.AlterField(
            model_name='cashplanpaymentverification',
            name='unicef_id',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
    ]
