# Generated by Django 2.2.16 on 2021-01-11 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp_datahub', '0011_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fundscommitment',
            name='ca_sync_flag',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='fundscommitment',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='fundscommitment',
            name='created_by',
            field=models.CharField(default='postgres', max_length=20),
        ),
        migrations.AlterField(
            model_name='fundscommitment',
            name='mis_sync_flag',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='fundscommitment',
            name='updated_by',
            field=models.CharField(default='postgres', max_length=20),
        ),
    ]