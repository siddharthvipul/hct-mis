# Generated by Django 3.2.20 on 2023-10-02 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0070_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datacollectingtype',
            name='compatible_types',
            field=models.ManyToManyField(blank=True, to='core.DataCollectingType'),
        ),
    ]
