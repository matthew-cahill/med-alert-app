# Generated by Django 4.2.11 on 2024-04-13 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("med_alert_app", "0009_report_resolved_action"),
    ]

    operations = [
        migrations.AddField(
            model_name="report",
            name="edited",
            field=models.BooleanField(default=False),
        ),
    ]
