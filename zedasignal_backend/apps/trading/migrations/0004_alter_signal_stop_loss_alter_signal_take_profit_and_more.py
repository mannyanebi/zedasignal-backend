# Generated by Django 4.2.4 on 2024-02-24 15:05

from django.db import migrations, models
import django_jsonform.models.fields


class Migration(migrations.Migration):
    dependencies = [
        ("trading", "0003_alter_signal_entry"),
    ]

    operations = [
        migrations.AlterField(
            model_name="signal",
            name="stop_loss",
            field=models.FloatField(help_text="The stop loss price of the signal.", verbose_name="stop loss"),
        ),
        migrations.AlterField(
            model_name="signal",
            name="take_profit",
            field=models.FloatField(help_text="The take profit price of the signal.", verbose_name="take profit"),
        ),
        migrations.AlterField(
            model_name="signal",
            name="targets",
            field=django_jsonform.models.fields.ArrayField(
                base_field=models.FloatField(), blank=True, help_text="Profit targets", null=True, size=None
            ),
        ),
    ]
