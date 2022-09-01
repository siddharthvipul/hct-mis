# Generated by Django 3.2.13 on 2022-08-30 11:44

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0060_migration"),
    ]

    operations = [
        migrations.AlterField(
            model_name="paymentplan",
            name="status",
            field=django_fsm.FSMField(
                choices=[
                    ("OPEN", "Open"),
                    ("LOCKED", "Locked"),
                    ("LOCKED_FSP", "Locked FSP"),
                    ("IN_APPROVAL", "In Approval"),
                    ("IN_AUTHORIZATION", "In Authorization"),
                    ("IN_REVIEW", "In Review"),
                    ("ACCEPTED", "Accepted"),
                    ("STEFICON_WAIT", "Waiting for Rule Engine"),
                    ("STEFICON_RUN", "Rule Engine Running"),
                    ("STEFICON_COMPLETED", "Rule Engine Completed"),
                    ("STEFICON_ERROR", "Rule Engine Errored"),
                    ("XLSX_EXPORTING", "Exporting XLSX file"),
                    ("XLSX_IMPORTING", "Importing XLSX file"),
                ],
                db_index=True,
                default="OPEN",
                max_length=50,
            ),
        ),
    ]
