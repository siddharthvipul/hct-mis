# Generated by Django 2.2.16 on 2021-01-21 23:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0044_migration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='household',
            options={'verbose_name': 'Household'},
        ),
        migrations.AlterModelOptions(
            name='individual',
            options={'verbose_name': 'Individual'},
        ),
    ]
