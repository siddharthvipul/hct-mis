# Generated by Django 2.2.8 on 2020-10-20 09:41

from django.db import migrations

from payment.models import PaymentRecord


def delivery_type_labels_to_valid_choices(apps, schema_editor):
    CashPlan = apps.get_model("program", "CashPlan")
    delivery_type_choices_dict = {value: key for key, value in PaymentRecord.DELIVERY_TYPE_CHOICE}
    all_cash_plans = CashPlan.objects.all()
    for cash_plan in all_cash_plans:
        cash_plan.delivery_type = delivery_type_choices_dict.get(
            cash_plan.delivery_type, PaymentRecord.DELIVERY_TYPE_CASH
        )
    CashPlan.objects.bulk_update(all_cash_plans, ["delivery_type"])

def empty_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("program", "0014_migration"),
    ]

    operations = [
        migrations.RunPython(delivery_type_labels_to_valid_choices, empty_reverse)
    ]
