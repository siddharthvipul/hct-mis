# Generated by Django 3.2.15 on 2022-10-12 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Changelog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True)),
                ('version', models.CharField(help_text='HOPE version', max_length=30)),
                ('active', models.BooleanField(default=False)),
                ('date', models.DateField(auto_now=True)),
            ],
            options={
                'ordering': ('date',),
            },
        ),
    ]
