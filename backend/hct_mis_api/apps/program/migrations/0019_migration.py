# Generated by Django 2.2.16 on 2021-02-01 19:58

from django.db import migrations, models
from decimal import Decimal


def populate_existing_cash_plan_rates(apps, schema_editor):
    CashPlan = apps.get_model("program", "CashPlan")
    FundsCommitment = apps.get_model("erp_datahub", "FundsCommitment")
    all_cash_plans = CashPlan.objects.all()

    for cash_plan in all_cash_plans:
        try:
            funds_commitment = FundsCommitment.objects.filter(
                funds_commitment_number=cash_plan.funds_commitment
            ).first()
            if not funds_commitment:
                continue
            cash_plan.exchange_rate = Decimal(
                funds_commitment.total_open_amount_usd / funds_commitment.total_open_amount_local
            ).quantize(Decimal(".00000001"))
        except Exception:
            pass
    CashPlan.objects.bulk_update(all_cash_plans, ["exchange_rate"])


def empty_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("program", "0018_migration"),
    ]

    operations = [
        migrations.AddField(
            model_name="cashplan",
            name="exchange_rate",
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=12, null=True),
        ),
        migrations.RunPython(populate_existing_cash_plan_rates, empty_reverse),
    ]