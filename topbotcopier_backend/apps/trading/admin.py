from typing import Any

from django.contrib import admin

from . import models


# Register your models here.
@admin.register(models.Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "min_investment_amount",
        "max_investment_amount",
        "performance_fee",
        "overall",
        "is_active",
        "is_top_performing",
    )
    readonly_fields = ("uuid",)
    ordering = ["-created_at"]


@admin.register(models.TopPerformingBot)
class TopPerformingBotAdmin(admin.ModelAdmin):
    list_display = (
        "bot",
        "price",
        "period",
    )
    readonly_fields = ("uuid",)
    ordering = ["-created_at"]


@admin.register(models.SubscriptionPlanPromo)
class SubscriptionPlanPromoAdmin(admin.ModelAdmin):
    list_display = ("name",)
    readonly_fields = ("uuid",)
    ordering = ["-created_at"]


@admin.register(models.SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "yearly_price",
        "is_active",
        "is_special",
    )
    readonly_fields = ("uuid",)
    ordering = ["-created_at"]


@admin.register(models.CopyTradingGuide)
class CopyTradingGuideAdmin(admin.ModelAdmin):
    list_display = (
        "bot",
        "description",
    )
    readonly_fields = ("uuid",)
    ordering = ["-created_at"]


@admin.register(models.AccountScreeningRequest)
class AccountScreeningRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "email", "phone_number", "is_approved")
    list_filter = ("user",)
    search_fields = (
        "user__email",
        "name",
        "phone_number",
        "email",
    )
    readonly_fields = ("uuid",)
    ordering = ["-created_at"]

    def save_model(self, request: Any, obj: models.AccountScreeningRequest, form: Any, change: Any) -> None:
        super().save_model(request, obj, form, change)
        models.AccountScreeningRequest.objects.filter(user=obj.user, is_approved=False).exclude(
            id=obj.id  # type: ignore
        ).delete()


@admin.register(models.BotlabBot)
class BotlabBotsAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "name_of_broker",
        "server_name",
    )
    readonly_fields = ("uuid",)
    ordering = ["-created_at"]


@admin.register(models.AccountUpgradePaymentRequest)
class AccountUpgradePaymentRequestAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "subscription_plan",
    )
    list_filter = (
        "subscription_plan",
        "user",
    )
    search_fields = ("user__email",)
    readonly_fields = (
        "uuid",
        "created_at",
        "updated_at",
    )
    ordering = ["-created_at"]
