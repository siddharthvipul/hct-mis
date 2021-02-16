# Generated by Django 2.2.16 on 2021-02-16 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp_datahub', '0013_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fundscommitment',
            name='commitment_amount_local',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='fundscommitment',
            name='commitment_amount_usd',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='fundscommitment',
            name='total_open_amount_local',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='fundscommitment',
            name='total_open_amount_usd',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
    ]
