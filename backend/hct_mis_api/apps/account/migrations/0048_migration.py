# Generated by Django 3.2.18 on 2023-03-06 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0047_migration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='role',
            options={'ordering': ('subsystem', 'name')},
        ),
    ]
