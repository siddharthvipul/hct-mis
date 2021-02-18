# Generated by Django 2.2.16 on 2021-02-16 13:11

import django.contrib.postgres.fields.citext
import django.core.validators
from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0053_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='documenttype',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='documenttype',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='documentvalidator',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='documentvalidator',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='entitlementcard',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='entitlementcard',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='household',
            name='country',
            field=django_countries.fields.CountryField(db_index=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='household',
            name='country_origin',
            field=django_countries.fields.CountryField(blank=True, db_index=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='household',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='household',
            name='size',
            field=models.PositiveIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='household',
            name='unhcr_id',
            field=models.CharField(blank=True, db_index=True, default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='household',
            name='unicef_id',
            field=django.contrib.postgres.fields.citext.CICharField(blank=True, db_index=True, default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='household',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='household',
            name='withdrawn',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='household',
            name='withdrawn_date',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='individual',
            name='birth_date',
            field=models.DateField(db_index=True),
        ),
        migrations.AlterField(
            model_name='individual',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='individual',
            name='duplicate',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='individual',
            name='family_name',
            field=django.contrib.postgres.fields.citext.CICharField(blank=True, db_index=True, max_length=85),
        ),
        migrations.AlterField(
            model_name='individual',
            name='full_name',
            field=django.contrib.postgres.fields.citext.CICharField(db_index=True, max_length=255, validators=[django.core.validators.MinLengthValidator(2)]),
        ),
        migrations.AlterField(
            model_name='individual',
            name='given_name',
            field=django.contrib.postgres.fields.citext.CICharField(blank=True, db_index=True, max_length=85),
        ),
        migrations.AlterField(
            model_name='individual',
            name='marital_status',
            field=models.CharField(choices=[('', 'None'), ('SINGLE', 'Single'), ('MARRIED', 'Married'), ('WIDOWED', 'Widowed'), ('DIVORCED', 'Divorced'), ('SEPARATED', 'Separated')], db_index=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='individual',
            name='middle_name',
            field=django.contrib.postgres.fields.citext.CICharField(blank=True, db_index=True, max_length=85),
        ),
        migrations.AlterField(
            model_name='individual',
            name='sex',
            field=models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female')], db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='individual',
            name='unicef_id',
            field=django.contrib.postgres.fields.citext.CICharField(blank=True, db_index=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='individual',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='individual',
            name='withdrawn',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='individualroleinhousehold',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='individualroleinhousehold',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
    ]
