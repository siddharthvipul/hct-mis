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
    ]