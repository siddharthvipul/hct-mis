# Generated by Django 2.2.8 on 2020-04-22 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration_datahub', '0013_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='importedhousehold',
            name='head_of_household',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='registration_datahub.ImportedIndividual'),
        ),
    ]
