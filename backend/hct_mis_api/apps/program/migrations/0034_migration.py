# Generated by Django 3.2.13 on 2022-07-11 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0046_migration'),
        ('program', '0033_migration'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(
                    name='CashPlan',
                ),
            ],
            database_operations=[
            ],
        )
    ]
