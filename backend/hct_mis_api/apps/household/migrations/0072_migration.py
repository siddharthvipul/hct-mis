# Generated by Django 2.2.16 on 2021-06-14 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0071_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agency',
            name='type',
            field=models.CharField(choices=[('WFP', 'WFP'), ('UNHCR', 'UNHCR')], max_length=100),
        ),
    ]