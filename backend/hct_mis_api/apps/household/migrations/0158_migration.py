# Generated by Django 3.2.20 on 2023-07-27 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0157_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='household',
            name='origin_unicef_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='individual',
            name='origin_unicef_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
