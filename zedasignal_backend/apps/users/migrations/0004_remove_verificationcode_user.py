# Generated by Django 4.2.4 on 2023-10-22 08:16

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_profile"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="verificationcode",
            name="user",
        ),
    ]
