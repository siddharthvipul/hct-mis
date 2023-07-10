# Generated by Django 3.2.19 on 2023-06-10 13:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0034_migration'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('geo', '0007_migration'),
        ('core', '0042_migration_squashed_0043_migration'),
        ('reporting', '0008_migration_squashed_0014_migration'),
        ('grievance', '0035_migration_squashed_0049_migration'),
        ('household', '0119_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessarea',
            name='custom_fields',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='countrycodemap',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='flexibleattribute',
            name='hint',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='flexibleattribute',
            name='label',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='flexibleattributechoice',
            name='label',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='flexibleattributegroup',
            name='label',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='flexibleattribute',
            name='type',
            field=models.CharField(choices=[('DATE', 'Date'), ('DECIMAL', 'Decimal'), ('IMAGE', 'Image'), ('INTEGER', 'Integer'), ('GEOPOINT', 'Geopoint'), ('SELECT_ONE', 'Select One'), ('SELECT_MANY', 'Select Many'), ('STRING', 'String')], max_length=16),
        ),
        migrations.AlterField(
            model_name='xlsxkobotemplate',
            name='status',
            field=models.CharField(choices=[('CONNECTION_FAILED', 'Connection failed'), ('PROCESSING', 'Processing'), ('SUCCESSFUL', 'Successful'), ('UNSUCCESSFUL', 'Unsuccessful'), ('UPLOADED', 'Uploaded')], max_length=200),
        ),
        migrations.AlterField(
            model_name='countrycodemap',
            name='country_new',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='geo.country'),
        ),
        migrations.AddField(
            model_name='businessarea',
            name='postpone_deduplication',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='businessarea',
            name='deduplication_ignore_withdraw',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='StorageFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(upload_to='files')),
                ('business_area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.businessarea')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('status', models.CharField(choices=[('Not processed', 'Not processed'), ('Processing', 'Processing'), ('Finished', 'Finished'), ('Failed', 'Failed')], default='Not processed', max_length=25)),
            ],
        ),
        migrations.RemoveField(
            model_name='businessarea',
            name='countries',
        ),
        migrations.RenameField(
            model_name='businessarea',
            old_name='countries_new',
            new_name='countries',
        ),
        migrations.AlterModelOptions(
            name='countrycodemap',
            options={'ordering': ('country_new',)},
        ),
        migrations.RemoveField(
            model_name='countrycodemap',
            name='country',
        ),
        migrations.AlterModelOptions(
            name='countrycodemap',
            options={'ordering': ('country',)},
        ),
        migrations.RenameField(
            model_name='countrycodemap',
            old_name='country_new',
            new_name='country',
        ),
        migrations.AlterUniqueTogether(
            name='adminarealevel',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='adminarealevel',
            name='business_area',
        ),
        migrations.RemoveField(
            model_name='adminarealevel',
            name='country',
        ),
        migrations.DeleteModel(
            name='AdminArea',
        ),
        migrations.DeleteModel(
            name='AdminAreaLevel',
        ),
        migrations.AddField(
            model_name='businessarea',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterModelManagers(
            name='flexibleattributegroup',
            managers=[
                ('_tree_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
