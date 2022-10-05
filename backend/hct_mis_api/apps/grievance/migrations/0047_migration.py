# Generated by Django 3.2.13 on 2022-07-27 12:44

from django.db import migrations


def set_household_unicef_id(apps, schema_editor):
    from hct_mis_api.apps.grievance.models import GrievanceTicket
    start = 10_000
    grievance_tickets = []
    i, count = 0, GrievanceTicket.objects.all().count() // start + 1
    while i <= count:
        batch = GrievanceTicket.objects.all().order_by("created_at")[start * i: start * (i + 1)]
        for grv in batch:
            ticket_details = getattr(grv, "ticket_details", None)
            if ticket_details:
                household = getattr(ticket_details, "household", None)
                if household:
                    grv.household_unicef_id = ticket_details.household.unicef_id
                    grievance_tickets.append(grv)
        GrievanceTicket.objects.bulk_update(grievance_tickets, ["household_unicef_id"])
        grievance_tickets = []
        i += 1


def delete_household_unicef_id(apps, schema_editor):
    GrievanceTicket = apps.get_model("grievance", "GrievanceTicket")
    start = 10_000
    grievance_tickets = []
    i, count = 0, GrievanceTicket.objects.all().count() // start + 1
    while i <= count:
        batch = GrievanceTicket.objects.all().order_by("created_at")[start * i: start * (i + 1)]
        for grv in batch:
            grv.household_unicef_id = None
            grievance_tickets.append(grv)
        GrievanceTicket.objects.bulk_update(grievance_tickets, ["household_unicef_id"])
        grievance_tickets = []
        i += 1


class Migration(migrations.Migration):

    dependencies = [
        ('grievance', '0046_migration'),
        ('household', '0111_migration'),
    ]

    operations = [
        migrations.RunPython(set_household_unicef_id, delete_household_unicef_id)
    ]