# Generated by Django 3.2.24 on 2024-02-16 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('program', '0040_migration'), ('program', '0041_migration'), ('program', '0042_migration'), ('program', '0043_migration'), ('program', '0044_migration')]

    dependencies = [
        ('program', '0039_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='is_visible',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterUniqueTogether(
            name='program',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='program',
            constraint=models.UniqueConstraint(condition=models.Q(('is_removed', False)), fields=('name', 'business_area', 'is_removed'), name='unique_for_program_if_not_removed'),
        ),
        migrations.AlterField(
            model_name='program',
            name='scope',
            field=models.CharField(blank=True, choices=[('FOR_PARTNERS', 'For partners'), ('UNICEF', 'Unicef')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='program',
            name='household_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='program',
            name='individual_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
