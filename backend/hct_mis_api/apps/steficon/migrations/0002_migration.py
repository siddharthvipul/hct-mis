# Generated by Django 2.2.16 on 2021-02-04 12:28
from django.contrib.postgres.operations import CITextExtension
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('steficon', '0001_migration'),
    ]

    operations = [
        CITextExtension()
    ]
