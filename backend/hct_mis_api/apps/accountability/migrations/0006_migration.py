# Generated by Django 3.2.15 on 2022-12-16 09:10

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountability', '0005_migration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feedback',
            options={'ordering': ('created_at',), 'verbose_name': 'Feedback'},
        ),
        migrations.AlterModelOptions(
            name='feedbackmessage',
            options={'ordering': ('created_at',), 'verbose_name': 'Feedback message'},
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ('created_at',), 'verbose_name': 'Message'},
        ),
        migrations.AlterModelOptions(
            name='survey',
            options={'ordering': ('created_at',), 'verbose_name': 'Survey'},
        ),
        migrations.AddField(
            model_name='survey',
            name='successful_rapid_pro_calls',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.JSONField(), default=list, size=None),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='unicef_id',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='unicef_id',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='unicef_id',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
    ]