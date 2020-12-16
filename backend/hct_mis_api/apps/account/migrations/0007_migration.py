# Generated by Django 2.2.16 on 2020-12-09 22:27

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0006_migration"),
    ]

    operations = [
        migrations.AlterField(
            model_name="role",
            name="permissions",
            field=account.models.ChoiceArrayField(
                base_field=models.CharField(
                    choices=[
                        ("RDI_VIEW_LIST", "RDI VIEW LIST"),
                        ("RDI_VIEW_DETAILS", "RDI VIEW DETAILS"),
                        ("RDI_IMPORT_DATA", "RDI IMPORT DATA"),
                        ("RDI_RERUN_DEDUPE", "RDI RERUN DEDUPE"),
                        ("RDI_MERGE_IMPORT", "RDI MERGE IMPORT"),
                        ("POPULATION_VIEW_HOUSEHOLDS_LIST", "POPULATION VIEW HOUSEHOLDS LIST"),
                        ("POPULATION_VIEW_HOUSEHOLDS_DETAILS", "POPULATION VIEW HOUSEHOLDS DETAILS"),
                        ("POPULATION_VIEW_INDIVIDUALS_LIST", "POPULATION VIEW INDIVIDUALS LIST"),
                        ("POPULATION_VIEW_INDIVIDUALS_DETAILS", "POPULATION VIEW INDIVIDUALS DETAILS"),
                        ("PRORGRAMME_VIEW_LIST_AND_DETAILS", "PRORGRAMME VIEW LIST AND DETAILS"),
                        ("PROGRAMME_VIEW_PAYMENT_RECORD_DETAILS", "PROGRAMME VIEW PAYMENT RECORD DETAILS"),
                        ("PROGRAMME_CREATE", "PROGRAMME CREATE"),
                        ("PROGRAMME_UPDATE", "PROGRAMME UPDATE"),
                        ("PROGRAMME_REMOVE", "PROGRAMME REMOVE"),
                        ("PROGRAMME_ACTIVATE", "PROGRAMME ACTIVATE"),
                        ("PROGRAMME_FINISH", "PROGRAMME FINISH"),
                        ("TARGETING_VIEW_LIST", "TARGETING VIEW LIST"),
                        ("TARGETING_VIEW_DETAILS", "TARGETING VIEW DETAILS"),
                        ("TARGETING_CREATE", "TARGETING CREATE"),
                        ("TARGETING_UPDATE", "TARGETING UPDATE"),
                        ("TARGETING_DUPLICATE", "TARGETING DUPLICATE"),
                        ("TARGETING_REMOVE", "TARGETING REMOVE"),
                        ("TARGETING_LOCK", "TARGETING LOCK"),
                        ("TARGETING_UNLOCK", "TARGETING UNLOCK"),
                        ("TARGETING_SEND", "TARGETING SEND"),
                        ("PAYMENT_VERIFICATION_VIEW_LIST", "PAYMENT VERIFICATION VIEW LIST"),
                        ("PAYMENT_VERIFICATION_VIEW_DETAILS", "PAYMENT VERIFICATION VIEW DETAILS"),
                        ("PAYMENT_VERIFICATION_CREATE", "PAYMENT VERIFICATION CREATE"),
                        ("PAYMENT_VERIFICATION_UPDATE", "PAYMENT VERIFICATION UPDATE"),
                        ("PAYMENT_VERIFICATION_ACTIVATE", "PAYMENT VERIFICATION ACTIVATE"),
                        ("PAYMENT_VERIFICATION_DISCARD", "PAYMENT VERIFICATION DISCARD"),
                        ("PAYMENT_VERIFICATION_FINISH", "PAYMENT VERIFICATION FINISH"),
                        ("PAYMENT_VERIFICATION_EXPORT", "PAYMENT VERIFICATION EXPORT"),
                        ("PAYMENT_VERIFICATION_IMPORT", "PAYMENT VERIFICATION IMPORT"),
                        ("PAYMENT_VERIFICATION_VERIFY", "PAYMENT VERIFICATION VERIFY"),
                        (
                            "PAYMENT_VERIFICATION_VIEW_PAYMENT_RECORD_DETAILS",
                            "PAYMENT VERIFICATION VIEW PAYMENT RECORD DETAILS",
                        ),
                        ("USER_MANAGEMENT_VIEW_LIST", "USER MANAGEMENT VIEW LIST"),
                        ("DASHBOARD_VIEW_HQ", "DASHBOARD VIEW HQ"),
                        ("DASHBOARD_VIEW_COUNTRY", "DASHBOARD VIEW COUNTRY"),
                        ("DASHBOARD_EXPORT", "DASHBOARD EXPORT"),
                    ],
                    max_length=255,
                ),
                blank=True,
                null=True,
                size=None,
            ),
        ),
    ]
