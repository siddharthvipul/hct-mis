# Generated by Django 2.2.8 on 2020-09-14 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grievance', '0002_migration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='createdBy',
        ),
        migrations.DeleteModel(
            name='Grievance',
        ),
        migrations.DeleteModel(
            name='Note',
        ),
    ]
