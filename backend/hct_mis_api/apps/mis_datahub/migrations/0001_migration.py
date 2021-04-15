# Generated by Django 2.2.8 on 2020-06-04 14:17

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
            name='TargetPopulationEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('household_unhcr_id', models.CharField(max_length=255, null=True)),
                ('individual_unhcr_id', models.CharField(max_length=255, null=True)),
                ('household_mis_id', models.UUIDField(null=True)),
                ('individual_mis_id', models.UUIDField(null=True)),
                ('target_population_mis_id', models.UUIDField()),
                ('vulnerability_score', models.DecimalField(blank=True, decimal_places=3, help_text='Written by a tool such as Corticon.', max_digits=6, null=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mis_datahub.Session')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TargetPopulation',
            fields=[
                ('mis_id', models.UUIDField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('population_type', models.CharField(default='HOUSEHOLD', max_length=20)),
                ('targeting_criteria', models.TextField()),
                ('active_households', models.PositiveIntegerField(default=0)),
                ('program_mis_id', models.UUIDField()),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mis_datahub.Session')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('mis_id', models.UUIDField(primary_key=True, serialize=False)),
                ('business_area', models.CharField(max_length=20)),
                ('ca_id', models.CharField(max_length=255)),
                ('ca_hash_id', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('scope', models.CharField(choices=[('FOR_PARTNERS', 'For partners'), ('UNICEF', 'Unicef')], max_length=50)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('description', models.CharField(max_length=255, null=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mis_datahub.Session')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Individual',
            fields=[
                ('mis_id', models.UUIDField(primary_key=True, serialize=False)),
                ('unhcr_id', models.CharField(max_length=255, null=True)),
                ('household_mis_id', models.UUIDField()),
                ('status', models.CharField(choices=[('INACTIVE', 'Inactive'), ('ACTIVE', 'Active')], max_length=50, null=True)),
                ('national_id_number', models.CharField(max_length=255, null=True)),
                ('full_name', models.CharField(max_length=255)),
                ('family_name', models.CharField(max_length=255, null=True)),
                ('given_name', models.CharField(max_length=255, null=True)),
                ('middle_name', models.CharField(max_length=255, null=True)),
                ('sex', models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female')], max_length=255)),
                ('date_of_birth', models.DateField()),
                ('estimated_date_of_birth', models.BooleanField()),
                ('relationship', models.CharField(choices=[('NON_BENEFICIARY', 'Not a Family Member. Can only act as a recipient.'), ('HEAD', 'Head of household (self)'), ('SON_DAUGHTER', 'Son / Daughter'), ('WIFE_HUSBAND', 'Wife / Husband'), ('BROTHER_SISTER', 'Brother / Sister'), ('MOTHER_FATHER', 'Mother / Father'), ('AUNT_UNCLE', 'Aunt / Uncle'), ('GRANDMOTHER_GRANDFATHER', 'Grandmother / Grandfather'), ('MOTHERINLAW_FATHERINLAW', 'Mother-in-law / Father-in-law'), ('DAUGHTERINLAW_SONINLAW', 'Daughter-in-law / Son-in-law'), ('SISTERINLAW_BROTHERINLAW', 'Sister-in-law / Brother-in-law'), ('GRANDDAUGHER_GRANDSON', 'Granddaughter / Grandson'), ('NEPHEW_NIECE', 'Nephew / Niece'), ('COUSIN', 'Cousin')], max_length=255, null=True)),
                ('role', models.CharField(choices=[('PRIMARY', 'Primary collector'), ('ALTERNATE', 'Alternate collector'), ('NO_ROLE', 'None')], max_length=255, null=True)),
                ('marital_status', models.CharField(choices=[('SINGLE', 'SINGLE'), ('MARRIED', 'Married'), ('WIDOW', 'Widow'), ('DIVORCED', 'Divorced'), ('SEPARATED', 'Separated')], max_length=255)),
                ('phone_number', models.CharField(max_length=14, null=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mis_datahub.Session')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Household',
            fields=[
                ('mis_id', models.UUIDField(primary_key=True, serialize=False)),
                ('unhcr_id', models.CharField(max_length=255, null=True)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive')], default='ACTIVE', max_length=20)),
                ('household_size', models.PositiveIntegerField()),
                ('form_number', models.CharField(max_length=255, null=True)),
                ('address', models.CharField(max_length=255, null=True)),
                ('admin1', models.CharField(max_length=255, null=True)),
                ('admin2', models.CharField(max_length=255, null=True)),
                ('country', django_countries.fields.CountryField(max_length=2, null=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mis_datahub.Session')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]