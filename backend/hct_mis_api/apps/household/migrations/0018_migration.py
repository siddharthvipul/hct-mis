# Generated by Django 2.2.8 on 2020-08-18 16:38

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0017_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='individual',
            name='deduplication_results',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]
