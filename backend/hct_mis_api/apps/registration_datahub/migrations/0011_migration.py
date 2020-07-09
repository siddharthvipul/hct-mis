# Generated by Django 2.2.8 on 2020-07-02 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration_datahub', '0010_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='importedindividual',
            name='work_status',
            field=models.CharField(blank=True, choices=[('YES', 'Yes'), ('NO', 'No'), ('NOT_PROVIDED', 'Not provided')], default='NOT_PROVIDED', max_length=20),
        ),
    ]
