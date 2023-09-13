# Generated by Django 3.2.20 on 2023-07-21 10:45

from django.db import migrations

def update_status_for_not_assigned_tickets(apps, schema_editor):
    from hct_mis_api.apps.grievance.models import GrievanceTicket

    GrievanceTicket.default_for_migrations_fix.filter(status=GrievanceTicket.STATUS_ASSIGNED, assigned_to=None).update(status=GrievanceTicket.STATUS_NEW)


class Migration(migrations.Migration):

    dependencies = [
        ('grievance', '0055_migration_squashed_0061_migration'),
    ]

    operations = [
        migrations.RunPython(update_status_for_not_assigned_tickets, migrations.RunPython.noop),
    ]
