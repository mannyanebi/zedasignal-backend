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
