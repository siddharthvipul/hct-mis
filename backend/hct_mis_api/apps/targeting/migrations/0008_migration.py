# Generated by Django 2.2.8 on 2020-06-17 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('targeting', '0007_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='targetpopulation',
            name='ca_hash_id',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='targetpopulation',
            name='ca_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]