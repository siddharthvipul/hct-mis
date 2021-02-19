# Generated by Django 2.2.16 on 2021-02-18 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("program", "0023_migration"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cashplan",
            name="delivery_type",
            field=models.CharField(
                choices=[
                    ("Cardless cash withdrawal", "Cardless cash withdrawal"),
                    ("Cash", "Cash"),
                    ("Cash by FSP", "Cash by FSP"),
                    ("Cheque", "Cheque"),
                    ("Deposit to Card", "Deposit to Card"),
                    ("In Kind", "In Kind"),
                    ("Mobile Money", "Mobile Money"),
                    ("Other", "Other"),
                    ("Pre-paid card", "Pre-paid card"),
                    ("Referral", "Referral"),
                    ("Transfer", "Transfer"),
                    ("Transfer to Account", "Transfer to Account"),
                    ("Voucher", "Voucher"),
                ],
                db_index=True,
                max_length=24,
                null=True,
            ),
        ),
    ]
