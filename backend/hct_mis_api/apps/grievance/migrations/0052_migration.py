# Generated by Django 3.2.15 on 2022-11-25 10:52
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("grievance", "0051_migration"),
    ]

    operations = [
        migrations.AlterField(
            model_name="grievanceticket",
            name="linked_tickets",
            field=models.ManyToManyField(
                related_name="_grievance_grievanceticket_linked_tickets_+",
                through="grievance.GrievanceTicketThrough",
                to="grievance.GrievanceTicket",
            ),
        ),
        migrations.AddConstraint(
            model_name="grievanceticketthrough",
            constraint=models.UniqueConstraint(
                fields=("main_ticket", "linked_ticket"), name="unique_main_linked_ticket"
            ),
        ),
    ]
