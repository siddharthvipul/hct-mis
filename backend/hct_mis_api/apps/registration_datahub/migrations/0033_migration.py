# Generated by Django 2.2.16 on 2020-12-30 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration_datahub', '0032_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importedindividual',
            name='pregnant',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
