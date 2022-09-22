# Generated by Django 3.2.15 on 2022-09-21 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0048_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashplanpaymentverification',
            name='error',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='paymentverification',
            name='sent_to_rapid_pro',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='cashplanpaymentverification',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'Active'), ('FINISHED', 'Finished'), ('PENDING', 'Pending'), ('INVALID', 'Invalid'), ('RAPID_PRO_ERROR', 'RapidPro Error')], db_index=True, default='PENDING', max_length=50),
        ),
    ]
