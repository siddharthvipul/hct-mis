# Generated by Django 3.2.23 on 2024-02-26 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('targeting', '0042_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='householdselection',
            name='is_original',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]
