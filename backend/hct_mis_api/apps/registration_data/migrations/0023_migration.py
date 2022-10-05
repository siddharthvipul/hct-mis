# Generated by Django 3.2.15 on 2022-09-21 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration_data', '0022_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationdataimport',
            name='data_source',
            field=models.CharField(choices=[('XLS', 'Excel'), ('KOBO', 'KoBo'), ('DIIA', 'DIIA'), ('FLEX_REGISTRATION', 'Flex Registration'), ('API', 'Flex API')], max_length=255),
        ),
        migrations.AlterField(
            model_name='registrationdataimport',
            name='status',
            field=models.CharField(choices=[('LOADING', 'Loading'), ('DEDUPLICATION', 'Deduplication'), ('DEDUPLICATION_FAILED', 'Deduplication Failed'), ('IMPORTING', 'Importing'), ('IMPORT_ERROR', 'Import Error'), ('IN_REVIEW', 'In Review'), ('MERGED', 'Merged'), ('MERGING', 'Merging'), ('MERGE_ERROR', 'Merge Error'), ('REFUSED', 'Refused import')], db_index=True, default='IN_REVIEW', max_length=255),
        ),
    ]