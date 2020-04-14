# Generated by Django 2.2.8 on 2020-04-10 09:11

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration_datahub', '0009_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='importedhousehold',
            name='flex_fields',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='importedindividual',
            name='flex_fields',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]
