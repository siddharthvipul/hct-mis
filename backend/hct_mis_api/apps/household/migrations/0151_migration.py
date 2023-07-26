# Generated by Django 3.2.20 on 2023-07-21 11:59

from django.db import migrations, models


def update_individual_relationship_typo(apps, schema_editor):
    # old name is 'GRANDDAUGHER_GRANDSON' new -> 'GRANDDAUGHTER_GRANDSON'
    Individual = apps.get_model("household", "Individual")
    Individual.objects.filter(relationship="GRANDDAUGHER_GRANDSON").update(relationship="GRANDDAUGHTER_GRANDSON")


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0150_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individual',
            name='relationship',
            field=models.CharField(blank=True, choices=[('UNKNOWN', 'Unknown'), ('AUNT_UNCLE', 'Aunt / Uncle'), ('BROTHER_SISTER', 'Brother / Sister'), ('COUSIN', 'Cousin'), ('DAUGHTERINLAW_SONINLAW', 'Daughter-in-law / Son-in-law'), ('GRANDDAUGHTER_GRANDSON', 'Granddaughter / Grandson'), ('GRANDMOTHER_GRANDFATHER', 'Grandmother / Grandfather'), ('HEAD', 'Head of household (self)'), ('MOTHER_FATHER', 'Mother / Father'), ('MOTHERINLAW_FATHERINLAW', 'Mother-in-law / Father-in-law'), ('NEPHEW_NIECE', 'Nephew / Niece'), ('NON_BENEFICIARY', 'Not a Family Member. Can only act as a recipient.'), ('OTHER', 'Other'), ('SISTERINLAW_BROTHERINLAW', 'Sister-in-law / Brother-in-law'), ('SON_DAUGHTER', 'Son / Daughter'), ('WIFE_HUSBAND', 'Wife / Husband'), ('FOSTER_CHILD', 'Foster child'), ('FREE_UNION', 'Free union')], help_text='This represents the MEMBER relationship. can be blank\n            as well if household is null!', max_length=255),
        ),
        migrations.RunPython(update_individual_relationship_typo, migrations.RunPython.noop),
    ]
