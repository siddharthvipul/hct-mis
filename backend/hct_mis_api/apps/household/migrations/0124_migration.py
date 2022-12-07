# Generated by Django 3.2.15 on 2022-10-02 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0123_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='geo.country'),
        ),
        migrations.AlterUniqueTogether(
            name='documenttype',
            unique_together=set(),
        ),
        migrations.RemoveConstraint(
            model_name='document',
            name='unique_if_not_removed_and_valid',
        ),
        migrations.AddConstraint(
            model_name='document',
            constraint=models.UniqueConstraint(condition=models.Q(models.Q(('is_removed', False), ('status', 'VALID'))), fields=('document_number', 'type', 'country'), name='unique_if_not_removed_and_valid'),
        ),
    ]