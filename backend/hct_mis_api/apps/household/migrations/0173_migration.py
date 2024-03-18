# Generated by Django 3.2.25 on 2024-03-18 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0172_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='household',
            name='head_of_household',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='heading_household', to='household.individual'),
        ),
    ]
