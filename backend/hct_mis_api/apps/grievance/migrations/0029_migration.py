# Generated by Django 2.2.16 on 2021-06-24 09:21

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('grievance', '0028_migration'),
    ]

    operations = [
        migrations.RunSQL(
            "ALTER TABLE grievance_grievanceticket ADD unicef_id_index SERIAL",
            "ALTER TABLE grievance_grievanceticket DROP unicef_id_index"
        ),
        migrations.RunSQL(
            """
            CREATE OR REPLACE FUNCTION create_gt_unicef_id() RETURNS trigger
                LANGUAGE plpgsql
                AS $$
            begin
              NEW.unicef_id := format('GRV-%s', trim(to_char(NEW.unicef_id_index,'000000')));
              return NEW;
            end
            $$;
    
            CREATE TRIGGER create_gt_unicef_id 
                BEFORE INSERT 
                ON grievance_grievanceticket 
                FOR EACH ROW 
            EXECUTE PROCEDURE create_gt_unicef_id();
            """,
            """
            DROP TRIGGER IF EXISTS create_gt_unicef_id ON grievance_grievanceticket
            """
        ),
        migrations.RunSQL(
            """
            UPDATE grievance_grievanceticket 
            SET unicef_id = format('GRV-%s', trim(to_char(unicef_id_index,'000000')));
            """,
            ""  # Needed to rollback migration
        ),
    ]