# Generated by Django 2.2.8 on 2020-04-24 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration_datahub', '0016_migration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='importedindividual',
            name='id_type',
        ),
    ]
