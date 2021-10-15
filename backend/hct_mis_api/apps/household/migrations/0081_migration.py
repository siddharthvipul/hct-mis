# Generated by Django 2.2.16 on 2021-08-30 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0080_migration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agency',
            options={'verbose_name_plural': 'Agencies'},
        ),
        migrations.AddField(
            model_name='individual',
            name='child_hoh',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='individual',
            name='fchild_hoh',
            field=models.BooleanField(default=False),
        ),
    ]