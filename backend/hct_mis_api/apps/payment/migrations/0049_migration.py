# Generated by Django 3.2.13 on 2022-07-26 14:58

from decimal import Decimal
from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0048_migration"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
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
                max_length=24,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="paymentrecord",
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
                max_length=24,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="payment",
            name="delivered_quantity",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=12,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0.01"))],
            ),
        ),
        migrations.AlterField(
            model_name="payment",
            name="entitlement_quantity",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=12,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0.01"))],
            ),
        ),
        migrations.AlterField(
            model_name="paymentrecord",
            name="delivered_quantity",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=12,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0.01"))],
            ),
        ),
        migrations.AlterField(
            model_name="paymentrecord",
            name="entitlement_quantity",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=12,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0.01"))],
            ),
        ),
    ]
