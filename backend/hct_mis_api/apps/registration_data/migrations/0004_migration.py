# Generated by Django 2.2.8 on 2020-06-23 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration_data', '0003_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationdataimport',
            name='data_source',
            field=models.CharField(choices=[('XLS', 'Excel'), ('KOBO', 'KoBo')], max_length=255),
        ),
    ]
