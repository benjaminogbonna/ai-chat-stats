# Generated by Django 5.1.5 on 2025-01-18 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="data",
            field=models.FileField(default="", upload_to="data/"),
        ),
    ]
