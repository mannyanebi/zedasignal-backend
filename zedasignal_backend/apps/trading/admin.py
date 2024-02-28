from django.contrib import admin

from zedasignal_backend.apps.trading import models


# Register your models here.
@admin.register(models.Signal)
class SignalAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "entry",
        "take_profit",
        "stop_loss",
        "term",
        "action",
        "pair_base",
        "pair_quote",
        "created_at",
    )
    readonly_fields = ("uuid", "created_at")


@admin.register(models.SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "monthly_price",
        "yearly_price",
        "created_at",
    )
    readonly_fields = ("uuid", "created_at")


@admin.register(models.Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "start_timestamp",
        "end_timestamp",
        "is_active",
        "created_at",
    )
    readonly_fields = ("uuid", "created_at")
