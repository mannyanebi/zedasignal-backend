# Generated by Django 4.2.4 on 2024-02-24 15:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("trading", "0002_alter_signal_entry_alter_signal_stop_loss_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="signal",
            name="entry",
            field=models.FloatField(help_text="The entry price of the signal.", verbose_name="entry"),
        ),
    ]
