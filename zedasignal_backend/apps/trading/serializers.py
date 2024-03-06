from rest_framework import serializers

from zedasignal_backend.apps.users.api.serializers import UserSerializer

from .models import Signal, SubscriptionPlan


class SignalReadSerializer(serializers.ModelSerializer[Signal]):
    author = UserSerializer()

    class Meta:
        model = Signal
        exclude = (
            "id",
            "targets",
        )


class SignalCreateSerializer(serializers.ModelSerializer[Signal]):
    class Meta:
        model = Signal
        exclude = (
            "id",
            "uuid",
            "author",
            "targets",
            "is_active",
            "created_at",
            "updated_at",
        )


class SubscriptionPlanReadSerializer(serializers.ModelSerializer[SubscriptionPlan]):
    class Meta:
        model = SubscriptionPlan
        exclude = (
            "id",
            "creator",
        )


class UserActiveSubscriptionPlanReadSerializer(serializers.Serializer):
    plan = SubscriptionPlanReadSerializer()
    active = serializers.BooleanField()


class UserAndActiveSubscriptionPlanReadSerializer(serializers.Serializer):
    user = UserSerializer()
    subscription_plan = SubscriptionPlanReadSerializer()
