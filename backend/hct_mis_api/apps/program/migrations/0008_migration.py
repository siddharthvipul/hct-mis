# Generated by Django 2.2.8 on 2020-06-18 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0007_migration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cashplan',
            name='last_sync_at',
        ),
        migrations.AddField(
            model_name='program',
            name='last_sync_at',
            field=models.DateTimeField(null=True),
        ),
    ]
