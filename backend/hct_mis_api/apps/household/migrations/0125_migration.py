# Generated by Django 3.2.15 on 2022-09-19 23:40

from django.db import migrations

from hct_mis_api.apps.household.models import IDENTIFICATION_TYPE_CHOICE


def migrate_doc_type(apps, schema_editor):
    # Country = apps.get_model('geo', 'Country')
    # Document = apps.get_model('household', 'Document')
    # DocumentType = apps.get_model('household', 'DocumentType')
    #
    # for country in Country.objects.all():
    #     Document.objects.filter(type__country=country).update(country=country)
    #
    # tostay = Country.objects.first()
    # for code, _ in IDENTIFICATION_TYPE_CHOICE:
    #     new_type, _ = DocumentType.objects.get_or_create(type=code, country=tostay, defaults={'label': code})
    #     Document.objects.filter(type__type=code).update(type=new_type)
    # DocumentType.objects.exclude(country=tostay).delete()
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0124_migration'),
    ]

    operations = [
        migrations.RunPython(migrate_doc_type, migrations.RunPython.noop),
    ]
