# Generated by Django 3.2.24 on 2024-02-16 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('reporting', '0015_migration'), ('reporting', '0016_migration'), ('reporting', '0017_migration')]

    dependencies = [
        ('reporting', '0008_migration_squashed_0014_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboardreport',
            name='year',
            field=models.PositiveSmallIntegerField(default=2023),
        ),
        migrations.AlterField(
            model_name='report',
            name='report_type',
            field=models.IntegerField(choices=[(1, 'Individuals'), (2, 'Households'), (3, 'Cash Plan Verification'), (4, 'Payments'), (5, 'Payment verification'), (10, 'Payment Plan'), (6, 'Cash Plan'), (7, 'Programme'), (8, 'Individuals & Payment'), (9, 'Grievances')]),
        ),
        migrations.AlterField(
            model_name='dashboardreport',
            name='year',
            field=models.PositiveSmallIntegerField(default=2024),
        ),
    ]