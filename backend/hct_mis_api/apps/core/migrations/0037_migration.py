# Generated by Django 2.2.16 on 2021-07-15 06:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_migration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='businessarea',
            options={'ordering': ['name'], 'permissions': (('can_split', 'Can split BusinessArea'), ('can_send_doap', 'Can send DOAP matrix'), ('can_reset_doap', 'Can force sync DOAP matrix'), ('can_export_doap', 'Can export DOAP matrix'))},
        ),
    ]
