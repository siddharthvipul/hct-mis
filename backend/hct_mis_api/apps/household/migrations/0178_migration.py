# Generated by Django 3.2.25 on 2024-05-26 15:13
import django
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0177_migration'),
        ('registration_data', '0038_migration')
    ]

    operations = [
        migrations.AddField(
            model_name='bankaccountinfo',
            name='rdi_merge_status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('MERGED', 'Merged')], default='PENDING', max_length=10),
        ),
        migrations.AddField(
            model_name='document',
            name='rdi_merge_status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('MERGED', 'Merged')], default='PENDING', max_length=10),
        ),
        migrations.AddField(
            model_name='household',
            name='rdi_merge_status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('MERGED', 'Merged')], default='PENDING', max_length=10),
        ),
        migrations.AddField(
            model_name='individual',
            name='rdi_merge_status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('MERGED', 'Merged')], default='PENDING', max_length=10),
        ),
        migrations.AddField(
            model_name='individualidentity',
            name='rdi_merge_status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('MERGED', 'Merged')], default='PENDING', max_length=10),
        ),
        migrations.AddField(
            model_name='individualroleinhousehold',
            name='rdi_merge_status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('MERGED', 'Merged')], default='PENDING', max_length=10),
        ),
        migrations.AlterField(
            model_name='household',
            name='head_of_household',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='heading_household', to='household.individual'),
        ),
        migrations.AddField(
            model_name='household',
            name='kobo_submission_time',
            field=models.DateTimeField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name="household",
            name="kobo_submission_uuid",
            field=models.UUIDField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='household',
            name='registration_id',
            field=django.contrib.postgres.fields.citext.CICharField(blank=True, db_index=True, max_length=100, null=True, verbose_name='Beneficiary Program Registration Id'),
        ),
        migrations.AddField(
            model_name='household',
            name='enumerator_rec_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='household',
            name='mis_unicef_id',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='individual',
            name='mis_unicef_id',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='household',
            name='flex_registrations_record',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='households', to='registration_data.record'),
        ),
    ]

