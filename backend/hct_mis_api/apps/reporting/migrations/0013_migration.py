# Generated by Django 3.2.13 on 2022-06-28 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0012_migration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='admin_area',
        ),
    ]