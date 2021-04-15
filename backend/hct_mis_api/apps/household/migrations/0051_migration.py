# Generated by Django 2.2.16 on 2021-02-12 10:58

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0050_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='household',
            name='flex_fields',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='household',
            name='last_sync_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='individual',
            name='flex_fields',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='individual',
            name='last_sync_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='individualroleinhousehold',
            name='last_sync_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]