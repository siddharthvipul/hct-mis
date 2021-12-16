# Generated by Django 2.2.16 on 2021-12-10 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration_datahub', '0047_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='importedindividual',
            name='kobo_asset_id',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
        migrations.AddField(
            model_name='importedhousehold',
            name='row_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='importedindividual',
            name='row_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
