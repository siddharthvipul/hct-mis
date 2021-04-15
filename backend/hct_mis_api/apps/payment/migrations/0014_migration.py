# Generated by Django 2.2.8 on 2020-08-24 15:47

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0013_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashplanpaymentverification',
            name='age_filter',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='cashplanpaymentverification',
            name='excluded_admin_areas_filter',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='cashplanpaymentverification',
            name='sex_filter',
            field=models.CharField(max_length=10, null=True),
        ),
    ]