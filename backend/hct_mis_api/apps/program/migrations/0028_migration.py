# Generated by Django 2.2.16 on 2021-08-30 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0027_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashplan',
            name='ca_id',
            field=models.CharField(db_index=True, max_length=255, null=True),
        ),
    ]
