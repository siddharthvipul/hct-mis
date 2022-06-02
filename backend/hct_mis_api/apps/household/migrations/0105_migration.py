# Generated by Django 3.2.12 on 2022-05-06 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0104_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='household',
            name='total_cash_received',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=64, null=True),
        ),
        migrations.AddField(
            model_name='household',
            name='total_cash_received_usd',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=64, null=True),
        ),
    ]