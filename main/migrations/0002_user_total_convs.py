# Generated by Django 5.1.5 on 2025-01-24 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="total_convs",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
