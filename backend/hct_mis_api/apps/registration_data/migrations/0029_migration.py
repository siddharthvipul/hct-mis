# Generated by Django 3.2.20 on 2023-09-04 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0038_migration'),
        ('registration_data', '0028_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrationdataimport',
            name='program',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='registration_imports', to='program.program'),
        ),
        migrations.AddField(
            model_name='registrationdataimport',
            name='programs',
            field=models.ManyToManyField(related_name='registration_data_imports', to='program.Program'),
        ),
    ]
