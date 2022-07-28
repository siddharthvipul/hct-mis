# Generated by Django 3.2.13 on 2022-07-19 12:07

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0109_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='individual',
            name='vector_column',
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
        migrations.AddIndex(
            model_name='individual',
            index=django.contrib.postgres.indexes.GinIndex(fields=['vector_column'], name='household_i_vector__4c5828_gin'),
        ),
    ]
