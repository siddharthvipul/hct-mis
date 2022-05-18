# Generated by Django 3.2.12 on 2022-05-16 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration_datahub', '0061_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='error_message',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='record',
            name='status',
            field=models.CharField(choices=[('TO_IMPORT', 'To import'), ('IMPORTED', 'Imported'), ('ERROR', 'Error')], null=True, blank=True, max_length=16),
        ),
    ]