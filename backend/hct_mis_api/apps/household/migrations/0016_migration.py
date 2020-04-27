# Generated by Django 2.2.8 on 2020-04-21 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_migration'),
        ('household', '0015_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='household',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Location'),
        ),
    ]
