from typing import Any

from rest_framework import serializers

from zedasignal_backend.apps.trading.models import (
    AccountScreeningRequest,
    AccountUpgradePaymentRequest,
    Bot,
    BotlabBot,
    CopyTradingGuide,
    SubscriptionPlan,
    SubscriptionPlanPromo,
    TopPerformingBot,
)
from zedasignal_backend.apps.users.api.serializers import UserSerializer


class BotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        exclude = ("created_at", "updated_at", "id")


class TopPerformingBotSerializer(serializers.ModelSerializer):
    bot = BotSerializer()

    class Meta:
        model = TopPerformingBot
        exclude = ("created_at", "updated_at", "id")


class SubscriptionPlanPromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlanPromo
        exclude = ("created_at", "updated_at", "id")


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    promos = SubscriptionPlanPromoSerializer(many=True, read_only=True)

    class Meta:
        model = SubscriptionPlan
        exclude = ("created_at", "updated_at", "id")


class CopyTradingGuideSerializer(serializers.ModelSerializer):
    bot = BotSerializer()

    class Meta:
        model = CopyTradingGuide
        exclude = ("created_at", "updated_at", "id")


class AccountScreeningRequestSerializer(
    serializers.ModelSerializer[AccountScreeningRequest]
):
    class Meta:
        model = AccountScreeningRequest
        exclude = (
            "created_at",
            "updated_at",
            "id",
            "user",
            "is_approved",
        )

        extra_kwargs = {
            "name": {"required": True},
            "email": {"required": True},
            "phone_number": {"required": True},
            "schedule_date": {"required": True},
            "schedule_time": {"required": True},
        }


class HelpSupportRequestSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    message = serializers.CharField(required=True)


class BotlabBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotlabBot
        exclude = (
            "created_at",
            "updated_at",
            "id",
        )


class CreateAccountUpgradePaymentRequestSerializer(
    serializers.ModelSerializer[AccountUpgradePaymentRequest]
):
    subscription_plan_uuid = serializers.UUIDField(required=True)

    class Meta:
        model = AccountUpgradePaymentRequest
        exclude = (
            "user",
            "subscription_plan",
            "created_at",
            "updated_at",
            "id",
        )

    def create(self, validated_data: Any) -> AccountUpgradePaymentRequest:
        subscription_plan_uuid = validated_data.pop("subscription_plan_uuid")
        try:
            subscription_plan = SubscriptionPlan.objects.get(
                uuid=subscription_plan_uuid
            )
        except SubscriptionPlan.DoesNotExist:
            raise serializers.ValidationError("Subscription plan does not exist")
        validated_data["subscription_plan"] = subscription_plan
        return super().create(validated_data)


class ReadAccountUpgradePaymentRequestSerializer(
    serializers.ModelSerializer[AccountUpgradePaymentRequest]
):
    subscription_plan = SubscriptionPlanSerializer()
    user = UserSerializer()

    class Meta:
        model = AccountUpgradePaymentRequest
        exclude = (
            "updated_at",
            "id",
        )
