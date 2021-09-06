# Generated by Django 2.2.16 on 2021-07-05 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0022_migration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': (('can_load_from_ad', 'Can load users from ActiveDirectory'), ('can_sync_with_ad', 'Can synchronise user with ActiveDirectory'), ('can_upload_to_kobo', 'Can upload users to Kobo'), ('can_import_from_kobo', 'Can import and sync users from Kobo'), ('can_debug', 'Can access debug informations'), ('can_inspect', 'Can inspect objects'))},
        ),
    ]