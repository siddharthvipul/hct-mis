# Generated by Django 3.2.24 on 2024-02-16 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('core', '0058_migration'), ('core', '0059_migration')]

    dependencies = [
        ('core', '0044_migration_squashed_0057_migration'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='flexibleattributegroup',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='businessarea',
            name='kobo_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='businessarea',
            name='kobo_url',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]
