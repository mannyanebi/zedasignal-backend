# Generated by Django 4.2.4 on 2023-10-30 19:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("trading", "0008_alter_subscriptionplan_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="accountscreeningrequest",
            name="country",
            field=models.CharField(
                blank=True,
                help_text="The country of the user requesting for account screening.",
                max_length=255,
                null=True,
                verbose_name="country",
            ),
        ),
        migrations.AddField(
            model_name="accountscreeningrequest",
            name="has_trading_experience",
            field=models.BooleanField(
                default=False,
                help_text="Designates whether the user requesting for account screening has trading experience.",
                verbose_name="has trading experience",
            ),
        ),
        migrations.AddField(
            model_name="accountscreeningrequest",
            name="previously_used_forex_broker",
            field=models.CharField(
                blank=True,
                help_text="The previously used forex broker of the user requesting for account screening.",
                max_length=255,
                null=True,
                verbose_name="previously used forex broker",
            ),
        ),
        migrations.AddField(
            model_name="accountscreeningrequest",
            name="trading_capital_amount",
            field=models.CharField(
                blank=True,
                help_text="The trading capital amount of the user requesting for account screening.",
                max_length=255,
                null=True,
                verbose_name="trading capital amount",
            ),
        ),
    ]
