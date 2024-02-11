# Generated by Django 4.2.4 on 2023-10-19 23:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="verificationcode",
            name="phone_number",
        ),
        migrations.AddField(
            model_name="verificationcode",
            name="email",
            field=models.EmailField(
                blank=True,
                help_text="The email to which the code was sent.",
                max_length=255,
                null=True,
                verbose_name="email",
            ),
        ),
    ]
