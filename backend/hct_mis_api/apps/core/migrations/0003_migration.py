# Generated by Django 2.2.8 on 2020-02-13 19:23

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import model_utils.fields
import mptt.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_migration'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlexibleAttributeGroup',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_removed', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('label', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('required', models.BooleanField(default=False)),
                ('repeatable', models.BooleanField(default=False)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='core.FlexibleAttributeGroup', verbose_name='Parent')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FlexibleAttribute',
            fields=[
                ('is_removed', models.BooleanField(default=False)),
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[('STRING', 'String'), ('IMAGE', 'Image'), ('INTEGER', 'Integer'), ('DECIMAL', 'Decimal'), ('SELECT_ONE', 'Select One'), ('SELECT_MANY', 'Select Many'), ('DATETIME', 'Datetime'), ('GEOPOINT', 'Geopoint')], max_length=16)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('required', models.BooleanField(default=False)),
                ('label', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('hint', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='flex_attributes', to='core.FlexibleAttributeGroup')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FlexibleAttributeChoice',
            fields=[
                ('is_removed', models.BooleanField(default=False)),
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('list_name', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('label', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('admin', models.CharField(max_length=255)),
                ('flex_attributes', models.ManyToManyField(to='core.FlexibleAttribute')),
            ],
            options={
                'unique_together': {('list_name', 'name')},
            },
        ),
    ]
