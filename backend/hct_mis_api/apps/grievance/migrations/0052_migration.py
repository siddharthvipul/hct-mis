# Generated by Django 3.2.15 on 2022-11-25 10:52
from django.core.paginator import Paginator
from django.db import migrations, models


def populate_symmetrical_relation_objects(apps, schema_editor):
    GrievanceTicketThrough = apps.get_model("grievance", "GrievanceTicketThrough")

    queryset = GrievanceTicketThrough.objects.all().order_by("pk")
    paginator = Paginator(queryset, 10000)

    for page_number in paginator.page_range:
        to_create = []

        page = paginator.page(page_number)
        for gtt in page.object_list:
            to_create.append(
                GrievanceTicketThrough(
                    main_ticket=gtt.linked_ticket,
                    linked_ticket=gtt.main_ticket,
                )
            )

        GrievanceTicketThrough.objects.bulk_create(to_create, ignore_conflicts=True)


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
        migrations.RunPython(populate_symmetrical_relation_objects, migrations.RunPython.noop),
    ]
