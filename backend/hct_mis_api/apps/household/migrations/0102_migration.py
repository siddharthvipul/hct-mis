# Generated by Django 3.2.12 on 2022-04-14 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0101_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccountinfo',
            name='debit_card_number',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
