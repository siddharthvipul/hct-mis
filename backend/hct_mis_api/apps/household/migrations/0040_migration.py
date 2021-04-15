# Generated by Django 2.2.16 on 2020-12-17 22:09

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0039_migration'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='individual',
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='individual',
            name='is_removed',
            field=models.BooleanField(default=False),
        ),
    ]