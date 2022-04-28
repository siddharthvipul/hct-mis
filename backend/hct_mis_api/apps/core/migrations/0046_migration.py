# Generated by Django 3.2.12 on 2022-03-31 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0007_migration'),
        ('core', '0045_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countrycodemap',
            name='country_new',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='geo.country'),
        ),
    ]