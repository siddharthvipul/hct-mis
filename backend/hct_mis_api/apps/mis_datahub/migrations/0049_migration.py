# Generated by Django 3.2.23 on 2024-01-31 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mis_datahub', '0048_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='programme_code',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='program',
            unique_together={('business_area', 'programme_code'), ('session', 'mis_id')},
        ),
    ]
