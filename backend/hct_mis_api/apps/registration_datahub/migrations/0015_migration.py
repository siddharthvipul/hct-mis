# Generated by Django 2.2.8 on 2020-04-22 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration_datahub', '0014_migration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='importedhousehold',
            name='household_ca_id',
        ),
        migrations.RemoveField(
            model_name='importedindividual',
            name='individual_ca_id',
        ),
    ]
