# Generated by Django 3.2.19 on 2023-06-28 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0060_migration_squashed_0064_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessarea',
            name='is_accountability_applicable',
            field=models.BooleanField(default=False),
        ),
    ]
