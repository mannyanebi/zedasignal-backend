# Generated by Django 4.2.4 on 2024-03-06 05:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("trading", "0007_signal_pair_base_signal_pair_quote"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="subscriptionplan",
            options={"ordering": ["ordering"]},
        ),
        migrations.AddField(
            model_name="subscriptionplan",
            name="ordering",
            field=models.PositiveIntegerField(
                default=0, help_text="The ordering of the subscription plan.", verbose_name="ordering"
            ),
        ),
    ]