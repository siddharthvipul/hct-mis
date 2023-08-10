# Generated by Django 3.2.19 on 2023-06-10 13:05

from decimal import Decimal
from typing import List, Dict, Any, Tuple

import django.core.validators
from django.db import migrations, models
import django.db.migrations.operations.special
import django.db.models.deletion
import model_utils.fields
import uuid


def _get_min_max_score(golden_records: List[Dict[str, Any]]) -> Tuple[float, float]:
    items = [item.get("score", 0.0) for item in golden_records]

    return min(items, default=0.0), max(items, default=0.0)


def update_min_max_score(apps, schema_editor):
    TicketNeedsAdjudicationDetails = apps.get_model("grievance", "TicketNeedsAdjudicationDetails")

    db_alias = schema_editor.connection.alias
    index = 0
    for ticket in TicketNeedsAdjudicationDetails.objects.using(db_alias).only("extra_data").iterator(1000):
        index += 1
        if index % 100 == 0:
            print(index)
        score_min, score_max = _get_min_max_score(ticket.extra_data.get("golden_records", []))
        ticket.score_min = score_min
        ticket.score_max = score_max
        ticket.save(update_fields=("score_min", "score_max"))

def set_household_unicef_id(apps, schema_editor):
    GrievanceTicket = apps.get_model("grievance", "GrievanceTicket")
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
        ('grievance', '0001_migration_squashed_0034_migration'),
        ('household', '0111_migration'),
        ('payment', '0030_migration_squashed_0051_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grievanceticket',
            name='extras',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='ticketaddindividualdetails',
            name='individual_data',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='ticketdeleteindividualdetails',
            name='role_reassign_data',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='tickethouseholddataupdatedetails',
            name='household_data',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='ticketindividualdataupdatedetails',
            name='individual_data',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='ticketindividualdataupdatedetails',
            name='role_reassign_data',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='ticketneedsadjudicationdetails',
            name='extra_data',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='ticketneedsadjudicationdetails',
            name='role_reassign_data',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='ticketsystemflaggingdetails',
            name='role_reassign_data',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='grievanceticket',
            name='category',
            field=models.IntegerField(choices=[(2, 'Data Change'), (4, 'Grievance Complaint'), (8, 'Needs Adjudication'), (5, 'Negative Feedback'), (1, 'Payment Verification'), (7, 'Positive Feedback'), (6, 'Referral'), (3, 'Sensitive Grievance'), (9, 'System Flagging')], verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='grievanceticket',
            name='status',
            field=models.IntegerField(choices=[(1, 'New'), (2, 'Assigned'), (6, 'Closed'), (5, 'For Approval'), (3, 'In Progress'), (4, 'On Hold')], default=1, verbose_name='Status'),
        ),
        migrations.CreateModel(
            name='TicketDeleteHouseholdDetails',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('role_reassign_data', models.JSONField(default=dict)),
                ('approve_status', models.BooleanField(default=False)),
                ('household', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='delete_household_ticket_details', to='household.household')),
                ('ticket', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='delete_household_ticket_details', to='grievance.grievanceticket')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='ticketpaymentverificationdetails',
            name='approve_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ticketpaymentverificationdetails',
            name='new_received_amount',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
        migrations.AddField(
            model_name='ticketpaymentverificationdetails',
            name='payment_verification',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ticket_detail', to='payment.paymentverification'),
        ),
        migrations.AddField(
            model_name='ticketpaymentverificationdetails',
            name='new_status',
            field=models.CharField(choices=[('NOT_RECEIVED', 'NOT RECEIVED'), ('PENDING', 'PENDING'), ('RECEIVED', 'RECEIVED'), ('RECEIVED_WITH_ISSUES', 'RECEIVED WITH ISSUES')], default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='ticketpaymentverificationdetails',
            name='payment_verification_status',
            field=models.CharField(choices=[('NOT_RECEIVED', 'NOT RECEIVED'), ('PENDING', 'PENDING'), ('RECEIVED', 'RECEIVED'), ('RECEIVED_WITH_ISSUES', 'RECEIVED WITH ISSUES')], max_length=50),
        ),
        migrations.AddField(
            model_name='ticketneedsadjudicationdetails',
            name='score_max',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='ticketneedsadjudicationdetails',
            name='score_min',
            field=models.FloatField(default=0.0),
        ),
        migrations.RunPython(update_min_max_score, migrations.RunPython.noop),
        migrations.AddField(
            model_name='ticketneedsadjudicationdetails',
            name='is_multiple_duplicates_version',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ticketneedsadjudicationdetails',
            name='possible_duplicates',
            field=models.ManyToManyField(related_name='ticket_duplicates', to='household.Individual'),
        ),
        migrations.AddField(
            model_name='ticketneedsadjudicationdetails',
            name='selected_individuals',
            field=models.ManyToManyField(related_name='ticket_selected', to='household.Individual'),
        ),
        migrations.AddField(
            model_name='grievanceticket',
            name='ignored',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AddField(
            model_name='grievanceticket',
            name='household_unicef_id',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='grievanceticket',
            name='unicef_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.RunSQL(
            sql="\n            CREATE OR REPLACE FUNCTION create_gt_unicef_id() RETURNS trigger\n                LANGUAGE plpgsql\n                AS $$\n            begin\n              NEW.unicef_id := format('GRV-%s', trim(to_char(NEW.unicef_id_index,'0000000')));\n              return NEW;\n            end\n            $$;\n            ",
        ),
        migrations.RunSQL(
            sql="\n            UPDATE grievance_grievanceticket \n            SET unicef_id = format('GRV-%s', trim(to_char(unicef_id_index,'0000000')));\n            ",
            reverse_sql='',
        ),
        migrations.RunPython(set_household_unicef_id, delete_household_unicef_id),
        migrations.RemoveField(
            model_name='grievanceticket',
            name='admin2',
        ),
        migrations.RenameField(
            model_name='grievanceticket',
            old_name='admin2_new',
            new_name='admin2',
        ),
    ]
