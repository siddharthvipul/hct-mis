# Generated by Django 3.2.20 on 2023-09-06 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration_data', '0029_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrationdataimport',
            name='batch_duplicates',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='registrationdataimport',
            name='batch_possible_duplicates',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='registrationdataimport',
            name='batch_unique',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='registrationdataimport',
            name='golden_record_duplicates',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='registrationdataimport',
            name='golden_record_possible_duplicates',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='registrationdataimport',
            name='golden_record_unique',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
