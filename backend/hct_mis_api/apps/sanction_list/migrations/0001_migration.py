# Generated by Django 2.2.8 on 2020-06-26 14:29

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SanctionListIndividual',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('data_id', models.PositiveIntegerField()),
                ('version_num', models.PositiveIntegerField()),
                ('first_name', models.CharField(max_length=85)),
                ('second_name', models.CharField(max_length=85)),
                ('third_name', models.CharField(blank=True, default='', max_length=85)),
                ('full_name', models.CharField(max_length=255)),
                ('name_original_script', models.CharField(blank=True, default='', max_length=255)),
                ('un_list_type', models.CharField(blank=True, default='', max_length=100)),
                ('reference_number', models.CharField(max_length=50, unique=True)),
                ('listed_on', models.DateTimeField()),
                ('comments', models.TextField(blank=True, default='')),
                ('designation', models.TextField(blank=True, default='')),
                ('list_type', models.CharField(max_length=50)),
                ('quality', models.CharField(blank=True, default='', max_length=50)),
                ('alias_name', models.CharField(blank=True, default='', max_length=255)),
                ('street', models.CharField(blank=True, default='', max_length=255)),
                ('city', models.CharField(blank=True, default='', max_length=255)),
                ('state_province', models.CharField(blank=True, default='', max_length=255)),
                ('address_note', models.CharField(blank=True, default='', max_length=255)),
                ('date_of_birth', models.DateField(blank=True, default=None, null=True)),
                ('year_of_birth', models.PositiveIntegerField(default=None, null=True)),
                ('exact_date', models.BooleanField(default=True)),
                ('country_of_birth', django_countries.fields.CountryField(blank=True, default='', max_length=2)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SanctionListIndividualNationalities',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nationality', django_countries.fields.CountryField(max_length=2)),
                ('individual', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nationalities', to='sanction_list.SanctionListIndividual')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SanctionListIndividualDocument',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('document_number', models.CharField(max_length=255)),
                ('type_of_document', models.CharField(max_length=255)),
                ('date_of_issue', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('issuing_country', django_countries.fields.CountryField(blank=True, default='', max_length=2)),
                ('note', models.CharField(blank=True, default='', max_length=255)),
                ('individual', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='sanction_list.SanctionListIndividual')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SanctionListIndividualCountries',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('individual', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='countries', to='sanction_list.SanctionListIndividual')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]