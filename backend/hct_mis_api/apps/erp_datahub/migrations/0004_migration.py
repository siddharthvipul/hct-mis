# Generated by Django 2.2.8 on 2020-07-20 12:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp_datahub', '0003_migration'),
    ]

    operations = [
        migrations.RenameField(
            model_name='downpayment',
            old_name='down_payment_number',
            new_name='down_payment_reference',
        ),
    ]
