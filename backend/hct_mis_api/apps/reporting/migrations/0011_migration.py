# Generated by Django 3.2.13 on 2022-06-28 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("reporting", "0010_migration"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="dashboardreport",
            name="admin_area",
        ),
    ]
