from rest_framework import serializers

from zedasignal_backend.apps.users.api.serializers import UserSerializer
from zedasignal_backend.apps.users.utils import get_custom_user_model

from .models import Signal, Subscription, SubscriptionPlan

User = get_custom_user_model()


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
    id = serializers.IntegerField()
    user = UserSerializer()
    subscription_plan = SubscriptionPlanReadSerializer()


class CreateUserSubscriptionSerializer(serializers.ModelSerializer[Subscription]):
    plan = serializers.SlugRelatedField(
        slug_field="uuid",
        queryset=SubscriptionPlan.objects.all(),
        required=True,
        help_text="The subscription plan uuid to be created for the user.",
    )
    user = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all(),
        required=True,
        help_text="The user username to create the subscription for.",
    )

    class Meta:
        model = Subscription
        fields = (
            "plan",
            "user",
            "start_timestamp",
            "end_timestamp",
        )


class AdminDashboardStatistics(serializers.Serializer):
    total_users = serializers.IntegerField()
    total_signals_provided = serializers.IntegerField()
    total_active_subscriptions = serializers.IntegerField()
    total_admins = serializers.IntegerField()
