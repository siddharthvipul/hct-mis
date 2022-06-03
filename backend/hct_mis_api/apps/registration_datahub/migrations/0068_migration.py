# Generated by Django 3.2.13 on 2022-06-03 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration_datahub', '0067_migration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='diiahousehold',
            name='head_of_household',
        ),
        migrations.RemoveField(
            model_name='diiaindividual',
            name='household',
        ),
        migrations.AddField(
            model_name='diiaindividual',
            name='rec_id',
            field=models.CharField(blank=True, db_index=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='diiahousehold',
            name='rec_id',
            field=models.CharField(blank=True, db_index=True, max_length=20, null=True),
        ),
    ]
