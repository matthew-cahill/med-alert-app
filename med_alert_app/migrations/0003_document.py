# Generated by Django 4.2.10 on 2024-03-15 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("med_alert_app", "0002_alter_siteadmin_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="Document",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("upload_time", models.DateTimeField(auto_now_add=True)),
                ("upload", models.FileField(upload_to="")),
            ],
        ),
    ]