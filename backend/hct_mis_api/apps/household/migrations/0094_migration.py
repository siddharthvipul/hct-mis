# Generated by Django 3.2 on 2022-02-11 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0093_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agency',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='household',
            name='flex_fields',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='household',
            name='user_fields',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='individual',
            name='deduplication_batch_results',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='individual',
            name='deduplication_golden_record_results',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='individual',
            name='flex_fields',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='individual',
            name='user_fields',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='individualidentity',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]