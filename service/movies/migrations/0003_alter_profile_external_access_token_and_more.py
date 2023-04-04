# Generated by Django 4.1.3 on 2023-04-04 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0002_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="external_access_token",
            field=models.CharField(
                default="", max_length=120, verbose_name="external_access_token"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="external_refresh_token",
            field=models.CharField(
                default="", max_length=120, verbose_name="external_refresh_token"
            ),
        ),
    ]
