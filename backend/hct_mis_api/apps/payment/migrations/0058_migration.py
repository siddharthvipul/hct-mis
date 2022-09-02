# Generated by Django 3.2.13 on 2022-08-17 10:36

import django.contrib.postgres.fields.citext
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0057_migration"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="unicef_id",
            field=django.contrib.postgres.fields.citext.CICharField(blank=True, db_index=True, max_length=250),
        ),
    ]
