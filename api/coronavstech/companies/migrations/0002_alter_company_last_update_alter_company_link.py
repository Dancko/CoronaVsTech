# Generated by Django 4.1.7 on 2023-03-28 04:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("companies", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="last_update",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="company",
            name="link",
            field=models.URLField(blank=True, max_length=100),
        ),
    ]