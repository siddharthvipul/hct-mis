# Generated by Django 2.2.8 on 2020-08-13 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0016_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='individual',
            name='deduplication_status',
            field=models.CharField(default='UNIQUE', max_length=50),
        ),
    ]
