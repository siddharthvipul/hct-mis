# Generated by Django 3.2.13 on 2022-09-15 12:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('registration_data', '0022_migration'),
        ('targeting', '0031_migration'),
        ('household', '0119_migration'),
        ('core', '0054_migration'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('unicef_id', models.CharField(blank=True, max_length=255, null=True)),
                ('title', models.CharField(max_length=60)),
                ('body', models.TextField(max_length=1000)),
                ('number_of_recipients', models.PositiveIntegerField(default=0)),
                ('sampling_type', models.CharField(choices=[('FULL_LIST', 'Full list'), ('RANDOM', 'Random sampling')], default='FULL_LIST', max_length=50)),
                ('full_list_arguments', models.JSONField(blank=True, null=True)),
                ('random_sampling_arguments', models.JSONField(blank=True, null=True)),
                ('sample_size', models.PositiveIntegerField(null=True)),
                ('business_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.businessarea')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='messages', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('households', models.ManyToManyField(blank=True, related_name='messages', to='household.Household')),
                ('registration_data_import', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='messages', to='registration_data.registrationdataimport')),
                ('target_population', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='messages', to='targeting.targetpopulation')),
            ],
            options={
                'abstract': False,
            },
        ),
        # 
        migrations.RunSQL(
            sql="ALTER TABLE communication_message ADD unicef_id_index SERIAL;",
            reverse_sql="ALTER TABLE communication_message DROP unicef_id_index;",
        ),
        migrations.RunSQL(
            sql="""
        CREATE OR REPLACE FUNCTION create_message_unicef_id() RETURNS trigger
            LANGUAGE plpgsql
            AS $$
        BEGIN
            NEW.unicef_id := format('MSG-%s-%s', to_char(NEW.created_at, 'yy'), TRIM(CASE WHEN NEW.unicef_id_index > 9999 THEN NEW.unicef_id_index::varchar(64) ELSE to_char(NEW.unicef_id_index, '0000') END));
            return NEW;
        END
        $$;
        
        CREATE TRIGGER create_message_unicef_id BEFORE INSERT ON communication_message FOR EACH ROW EXECUTE PROCEDURE create_message_unicef_id();
        """,
            reverse_sql="""
            DROP TRIGGER create_message_unicef_id ON communication_message;
            DROP FUNCTION create_message_unicef_id();
            """,
        ),
        migrations.RunSQL(
            sql="UPDATE communication_message SET unicef_id = format('MSG-%s-%s', to_char(created_at, 'yy'), TRIM(CASE WHEN unicef_id_index > 9999 THEN unicef_id_index::varchar(64) ELSE to_char(unicef_id_index, '0000') END));",
            reverse_sql="UPDATE communication_message SET unicef_id = NULL;",
        )
    ]
