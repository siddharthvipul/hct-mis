# Generated by Django 2.2.16 on 2021-04-07 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_migration'),
        ('grievance', '0023_migration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grievanceticket',
            name='admin',
        ),
        migrations.AddField(
            model_name='grievanceticket',
            name='admin2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.AdminArea'),
        ),
    ]
