# Generated by Django 2.2.16 on 2020-12-23 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grievance', '0018_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketsystemflaggingdetails',
            name='sanction_list_individual',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='sanction_list.SanctionListIndividual'),
        ),
    ]