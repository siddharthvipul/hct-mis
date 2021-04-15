# Generated by Django 2.2.8 on 2020-06-19 07:14

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cash_assist_datahub', '0002_migration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('source', models.CharField(choices=[('MIS', 'HCT-MIS'), ('CA', 'Cash Assist')], max_length=3)),
                ('status', models.CharField(choices=[('NEW', 'New'), ('READY', 'Ready'), ('PROCESSING', 'Processing'), ('COMPLETED', 'Completed'), ('FAILED', 'Failed')], max_length=11)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TargetPopulation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mis_id', models.UUIDField()),
                ('ca_id', models.CharField(max_length=255)),
                ('ca_hash_id', models.UUIDField()),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cash_assist_datahub.Session')),
            ],
            options={
                'unique_together': {('session', 'mis_id')},
            },
        ),
        migrations.CreateModel(
            name='ServiceProvider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_area', models.CharField(max_length=20)),
                ('ca_id', models.CharField(max_length=255)),
                ('full_name', models.CharField(max_length=255)),
                ('short_name', models.CharField(max_length=4)),
                ('country', models.CharField(max_length=3)),
                ('vision_id', models.CharField(max_length=255)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cash_assist_datahub.Session')),
            ],
            options={
                'unique_together': {('session', 'ca_id')},
            },
        ),
        migrations.CreateModel(
            name='Programme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mis_id', models.UUIDField()),
                ('ca_id', models.CharField(max_length=255)),
                ('ca_hash_id', models.CharField(max_length=255)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cash_assist_datahub.Session')),
            ],
            options={
                'unique_together': {('session', 'mis_id')},
            },
        ),
        migrations.CreateModel(
            name='PaymentRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_area', models.CharField(max_length=20, null=True)),
                ('status', models.CharField(choices=[('SUCCESS', 'Sucess'), ('PENDING', 'Pending'), ('ERROR', 'Error')], max_length=255, null=True)),
                ('status_date', models.DateTimeField(null=True)),
                ('ca_id', models.CharField(max_length=255)),
                ('ca_hash_id', models.UUIDField()),
                ('registration_ca_id', models.CharField(max_length=255, null=True)),
                ('household_mis_id', models.UUIDField(null=True)),
                ('head_of_household_mis_id', models.UUIDField(null=True)),
                ('full_name', models.CharField(max_length=255, null=True)),
                ('total_persons_covered', models.IntegerField(null=True)),
                ('distribution_modality', models.CharField(max_length=255, null=True)),
                ('target_population_mis_id', models.UUIDField(null=True)),
                ('target_population_cash_assist_id', models.CharField(max_length=255, null=True)),
                ('entitlement_card_number', models.CharField(max_length=255, null=True)),
                ('entitlement_card_status', models.CharField(choices=[('SUCCESS', 'Sucess'), ('PENDING', 'Pending'), ('ERROR', 'Error')], default='PENDING', max_length=20, null=True)),
                ('entitlement_card_issue_date', models.DateField(null=True)),
                ('delivery_type', models.CharField(choices=[('CASH', 'Cash'), ('DEPOSIT_TO_CARD', 'Deposit to Card'), ('TRANSFER', 'Transfer')], default='CASH', max_length=20, null=True)),
                ('currency', models.CharField(max_length=4, null=True)),
                ('entitlement_quantity', models.DecimalField(decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('delivered_quantity', models.DecimalField(decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('delivery_date', models.DateTimeField(null=True)),
                ('service_provider_ca_id', models.CharField(max_length=255, null=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cash_assist_datahub.Session')),
            ],
            options={
                'unique_together': {('session', 'ca_id')},
            },
        ),
        migrations.CreateModel(
            name='CashPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_area', models.CharField(max_length=20, null=True)),
                ('cash_plan_id', models.CharField(max_length=255)),
                ('cash_plan_hash_id', models.UUIDField()),
                ('status', models.CharField(choices=[('Distribution Completed', 'Distribution Completed'), ('Distribution Completed with Errors', 'Distribution Completed with Errors'), ('Transaction Completed', 'Transaction Completed'), ('Transaction Completed with Errors', 'Transaction Completed with Errors')], max_length=255, null=True)),
                ('status_date', models.DateTimeField(null=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('distribution_level', models.CharField(max_length=255, null=True)),
                ('start_date', models.DateTimeField(null=True)),
                ('end_date', models.DateTimeField(null=True)),
                ('dispersion_date', models.DateTimeField(null=True)),
                ('coverage_duration', models.PositiveIntegerField(null=True)),
                ('coverage_unit', models.CharField(max_length=255, null=True)),
                ('comments', models.CharField(max_length=255, null=True)),
                ('program_mis_id', models.UUIDField(null=True)),
                ('delivery_type', models.CharField(max_length=255, null=True)),
                ('assistance_measurement', models.CharField(max_length=255, null=True)),
                ('assistance_through', models.CharField(max_length=255, null=True)),
                ('vision_id', models.CharField(max_length=255, null=True)),
                ('funds_commitment', models.CharField(max_length=255, null=True)),
                ('down_payment', models.CharField(max_length=255, null=True)),
                ('validation_alerts_count', models.IntegerField(null=True)),
                ('total_persons_covered', models.IntegerField(null=True)),
                ('total_persons_covered_revised', models.IntegerField(null=True)),
                ('payment_records_count', models.IntegerField(null=True)),
                ('total_entitled_quantity', models.DecimalField(decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('total_entitled_quantity_revised', models.DecimalField(decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('total_delivered_quantity', models.DecimalField(decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('total_undelivered_quantity', models.DecimalField(decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cash_assist_datahub.Session')),
            ],
            options={
                'unique_together': {('session', 'cash_plan_id')},
            },
        ),
    ]