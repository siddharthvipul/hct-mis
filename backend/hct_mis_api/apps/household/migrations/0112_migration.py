# Generated by Django 3.2.13 on 2022-07-26 13:50

import django.contrib.postgres.fields.citext
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0111_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='individual',
            name='last_name',
            field=django.contrib.postgres.fields.citext.CICharField(blank=True, db_index=True, max_length=85, null=True),
        ),
    ]
