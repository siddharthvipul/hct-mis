# Generated by Django 2.2.16 on 2021-01-18 10:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grievance', '0019_migration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='grievanceticket',
            options={'ordering': ('status', 'created_at'), 'verbose_name': 'Grievance Ticket'},
        ),
    ]