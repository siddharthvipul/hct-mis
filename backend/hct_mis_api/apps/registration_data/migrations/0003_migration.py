# Generated by Django 2.2.8 on 2020-05-11 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_migration'),
        ('registration_data', '0002_migration'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='registrationdataimport',
            unique_together={('name', 'business_area')},
        ),
    ]
