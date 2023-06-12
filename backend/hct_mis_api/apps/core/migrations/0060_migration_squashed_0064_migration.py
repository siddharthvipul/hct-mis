# Generated by Django 3.2.19 on 2023-06-10 12:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    replaces = [('core', '0060_migration'), ('core', '0061_migration'), ('core', '0062_migration'), ('core', '0063_migration'), ('core', '0064_migration')]

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0059_migration'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileTemp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('object_id', models.CharField(max_length=120, null=True)),
                ('file', models.FileField(upload_to='')),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('was_downloaded', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RunSQL(
            sql="\n            CREATE OR REPLACE FUNCTION payment_plan_business_area_seq() RETURNS trigger \n                LANGUAGE plpgsql\n                AS $$\n            begin\n                execute format('create sequence if not exists payment_plan_business_area_seq_%s', translate(NEW.id::text, '-','_'));\n                return NEW;\n            end\n            $$;\n\n            ",
        ),
        migrations.RunSQL(
            sql='CREATE TRIGGER payment_plan_business_area_seq AFTER INSERT ON core_businessarea FOR EACH ROW EXECUTE PROCEDURE payment_plan_business_area_seq();',
        ),
        migrations.RunSQL(
            sql="\n            CREATE OR REPLACE FUNCTION payment_business_area_seq() RETURNS trigger \n                LANGUAGE plpgsql\n                AS $$\n            begin\n                execute format('create sequence if not exists payment_business_area_seq_%s', translate(NEW.id::text, '-','_'));\n                return NEW;\n            end\n            $$;\n\n            ",
        ),
        migrations.RunSQL(
            sql='CREATE TRIGGER payment_business_area_seq AFTER INSERT ON core_businessarea FOR EACH ROW EXECUTE PROCEDURE payment_business_area_seq();',
        ),
        migrations.AddField(
            model_name='businessarea',
            name='is_payment_plan_applicable',
            field=models.BooleanField(default=False),
        ),
        migrations.RunSQL(
            sql="\n            create or replace function payment_plan_business_area_for_old_ba(id text)\n               returns text \n               language plpgsql\n              as\n            $$\n            declare \n            -- variable declaration\n            begin\n                execute format('create sequence if not exists payment_plan_business_area_seq_%s', translate(id::text, '-','_'));\n                RETURN id;\n            end;\n            $$\n            ",
        ),
        migrations.RunSQL(
            sql='SELECT id, payment_plan_business_area_for_old_ba(id::text) AS result FROM core_businessarea;',
        ),
        migrations.RunSQL(
            sql="\n            create or replace function payment_business_area_for_old_ba(id text)\n               returns text \n               language plpgsql\n              as\n            $$\n            declare \n            -- variable declaration\n            begin\n                execute format('create sequence if not exists payment_business_area_seq_%s', translate(id::text, '-','_'));\n                RETURN id;\n            end;\n            $$\n        ",
        ),
        migrations.RunSQL(
            sql='SELECT id, payment_business_area_for_old_ba(id::text) AS result FROM core_businessarea;',
        ),
    ]