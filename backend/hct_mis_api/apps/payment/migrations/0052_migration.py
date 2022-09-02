# Generated by Django 3.2.13 on 2022-07-18 10:08

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_fsm
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("household", "0109_migration"),
        ("payment", "0051_migration"),
    ]

    operations = [
        migrations.CreateModel(
            name="DeliveryMechanismPerPaymentPlan",
            fields=[
                (
                    "id",
                    model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                ("sent_date", models.DateTimeField()),
                ("status", django_fsm.FSMField(db_index=True, default="NOT_SENT", max_length=50)),
                ("delivery_mechanism_order", models.PositiveIntegerField()),
                (
                    "entitlement_quantity",
                    models.DecimalField(
                        db_index=True,
                        decimal_places=2,
                        max_digits=12,
                        null=True,
                        validators=[django.core.validators.MinValueValidator(Decimal("0.01"))],
                    ),
                ),
                (
                    "entitlement_quantity_usd",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=12,
                        null=True,
                        validators=[django.core.validators.MinValueValidator(Decimal("0.01"))],
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="created_delivery_mechanisms",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "delivery_mechanism",
                    models.CharField(
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
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "payment_plan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="delivery_mechanisms",
                        to="payment.paymentplan",
                    ),
                ),
                (
                    "sent_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="sent_delivery_mechanisms",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "financial_service_provider",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="delivery_mechanisms_per_payment_plan",
                        to="payment.financialserviceprovider",
                    ),
                ),
            ],
            options={
                "unique_together": {("payment_plan", "delivery_mechanism", "delivery_mechanism_order")},
            },
        ),
        migrations.AddConstraint(
            model_name="deliverymechanismperpaymentplan",
            constraint=models.UniqueConstraint(
                fields=("payment_plan", "delivery_mechanism"), name="unique payment_plan_delivery_mechanism"
            ),
        ),
        migrations.AddConstraint(
            model_name="deliverymechanismperpaymentplan",
            constraint=models.UniqueConstraint(
                fields=("payment_plan", "delivery_mechanism_order"), name="unique payment_plan_delivery_mechanism_order"
            ),
        ),
        migrations.AddField(
            model_name="payment",
            name="assigned_payment_channel",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="payment.paymentchannel"
            ),
        ),
    ]
