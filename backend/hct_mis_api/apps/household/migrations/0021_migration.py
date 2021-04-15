# Generated by Django 2.2.8 on 2020-08-27 14:00

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0020_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='individual',
            name='sanction_list_possible_match',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='individual',
            name='sanction_list_results',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]