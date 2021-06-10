# Generated by Django 2.2.16 on 2021-06-08 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0066_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agency',
            name='type',
            field=models.CharField(choices=[('UNHCR', 'UNHCR'), ('WFP', 'WFP')], max_length=100),
        ),
    ]
