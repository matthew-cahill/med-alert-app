# Generated by Django 4.2.11 on 2024-03-29 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('med_alert_app', '0004_remove_document_upload_time_report_document_report'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='date_time_of_offense',
            field=models.DateTimeField(),
        ),
    ]
