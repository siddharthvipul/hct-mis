# Generated by Django 3.2.13 on 2022-06-09 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0107_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='household',
            name='kobo_asset_id',
            field=models.CharField(blank=True, db_index=True, default='', max_length=150),
        ),
    ]
