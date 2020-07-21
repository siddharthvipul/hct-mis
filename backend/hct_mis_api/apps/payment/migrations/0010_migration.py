# Generated by Django 2.2.8 on 2020-07-17 07:20

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0009_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentverification',
            name='received_amount',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
    ]
