# Generated by Django 3.2.13 on 2022-06-28 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sanction_list', '0017_migration'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sanctionlistindividual',
            old_name='country_of_birth_new',
            new_name='country_of_birth',
        ),
    ]