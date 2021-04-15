# Generated by Django 2.2.16 on 2020-11-26 15:04

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grievance', '0013_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketdeleteindividualdetails',
            name='approve_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ticketdeleteindividualdetails',
            name='role_reassign_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='grievanceticket',
            name='linked_tickets',
            field=models.ManyToManyField(related_name='linked_tickets_related', through='grievance.GrievanceTicketThrough', to='grievance.GrievanceTicket'),
        ),
    ]