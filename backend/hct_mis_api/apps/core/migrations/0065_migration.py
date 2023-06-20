import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0064_migration"),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketPriority',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.IntegerField(choices=[(1, 'High'), (2, 'Medium'), (3, 'Low')], default='',
                                                 verbose_name='Priority')),
                ('urgency',
                 models.IntegerField(choices=[(1, 'Very urgent'), (2, 'Urgent'), (3, 'Not urgent')], default='',
                                     verbose_name='Urgency')),
                ('ticket_type', models.IntegerField(
                    choices=[(1, 'Needs Adjudication'), (2, 'Payment Verification'), (3, 'System Flagging')],
                    default='', verbose_name='Ticket type')),
                ('business_area',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets_priority',
                                   to='core.businessarea')),
            ],
            options={
                'unique_together': {('business_area', 'ticket_type')},
            },
        ),
    ]