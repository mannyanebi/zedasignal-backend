from typing import Any

import environ
from django.db.models import Q
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from zedasignal_backend.apps.trading.decorators import user_has_active_subscription
from zedasignal_backend.apps.trading.models import Signal, SubscriptionPlan
from zedasignal_backend.apps.trading.serializers import (
    CreateUserSubscriptionSerializer,
    SignalCreateSerializer,
    SignalReadSerializer,
    SubscriptionPlanReadSerializer,
    UserActiveSubscriptionPlanReadSerializer,
    UserAndActiveSubscriptionPlanReadSerializer,
)
from zedasignal_backend.apps.users.api.serializers import ErrorResponseSerializer, create_success_response_serializer
from zedasignal_backend.apps.users.utils import get_custom_user_model
from zedasignal_backend.core.custom_view_pagination import CustomPageNumberPagination
from zedasignal_backend.core.decorators import admin_required
from zedasignal_backend.core.error_response import ErrorResponse
from zedasignal_backend.core.sender import Sender
from zedasignal_backend.core.success_response import SuccessResponse
from zedasignal_backend.core.views_mixins import CustomReadOnlyViewSet

User = get_custom_user_model()
env = environ.Env()


# Create your views here.
class AdminCreateSignal(APIView):
    serializer_class = SignalCreateSerializer

    @extend_schema(
        request=serializer_class,
        responses={
            200: create_success_response_serializer(SignalCreateSerializer()),
            400: ErrorResponseSerializer,
        },
        tags=["Trading"],
        description="Create a signal.",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return ErrorResponse(details=serializer.errors, status=400, message="Invalid data")
        signal = serializer.save(author=request.user)
        return SuccessResponse(data=self.serializer_class(signal).data, message="Signal created.")


@extend_schema_view(
    list=extend_schema(
        responses={
            200: create_success_response_serializer(SignalReadSerializer()),
            404: ErrorResponseSerializer,
        },
        tags=["Trading"],
        operation_id="ListSignals",
        description="List all signals.",
    ),
    retrieve=extend_schema(
        responses={
            200: create_success_response_serializer(SignalReadSerializer()),
            404: ErrorResponseSerializer,
        },
        tags=["Trading"],
        operation_id="RetrieveSignal",
        description="Retrieve a signal.",
    ),
)
class SignalModelViewSet(CustomReadOnlyViewSet):
    """
    Signal model viewset for Zedasignal Backend.
    """

    serializer_class = SignalReadSerializer
    queryset = Signal.objects.filter(is_active=True).order_by("-updated_at")
    lookup_field = "uuid"

    @user_has_active_subscription
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().list(request, *args, **kwargs)

    @user_has_active_subscription
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().retrieve(request, *args, **kwargs)


@extend_schema_view(
    list=extend_schema(
        responses={
            200: create_success_response_serializer(SubscriptionPlanReadSerializer()),
            404: ErrorResponseSerializer,
        },
        tags=["Trading"],
        operation_id="ListSubscriptionPlans",
        description="List all subscription plans.",
    ),
    retrieve=extend_schema(
        responses={
            200: create_success_response_serializer(SubscriptionPlanReadSerializer()),
            404: ErrorResponseSerializer,
        },
        tags=["Trading"],
        operation_id="RetrieveSubscriptionPlan",
        description="Retrieve a subscription plan.",
    ),
)
class SubscriptionPlanViewSet(CustomReadOnlyViewSet):
    """
    Subscription plan viewset for Zedasignal Backend.
    """

    serializer_class = SubscriptionPlanReadSerializer
    queryset = SubscriptionPlan.objects.filter(Q(is_active=True) | Q(coming_soon=True))
    lookup_field = "uuid"
    permission_classes = [AllowAny]


class UserActiveSubscriptionPlans(APIView):
    """
    User active subscription plans view for Zedasignal Backend.
    """

    serializer_class = UserActiveSubscriptionPlanReadSerializer

    @extend_schema(
        operation_id="UserActiveSubscriptionPlan",
        responses={
            200: create_success_response_serializer(UserActiveSubscriptionPlanReadSerializer()),
            400: ErrorResponseSerializer,
        },
        tags=["Trading"],
        description="Get user active subscription plans.",
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        all_subscriptions = SubscriptionPlan.objects.all()
        user_subscriptions = user.subscriptions.filter(is_active=True)

        subscription_status_list = [
            {
                "plan": SubscriptionPlanReadSerializer(plan).data,
                "active": user_subscriptions.filter(plan_id=plan.id).exists(),
            }
            for plan in all_subscriptions
        ]

        return SuccessResponse(data=subscription_status_list, message="User active subscription plans.")


@extend_schema_view(
    list=extend_schema(
        responses={
            200: create_success_response_serializer(UserAndActiveSubscriptionPlanReadSerializer()),
            404: ErrorResponseSerializer,
        },
        tags=["Trading"],
        operation_id="ListUsersAndActiveSubscriptionPlans",
        description="List all users and their active subscription plans.",
    ),
    retrieve=extend_schema(
        responses={
            200: create_success_response_serializer(UserAndActiveSubscriptionPlanReadSerializer()),
            404: ErrorResponseSerializer,
        },
        tags=["Trading"],
        operation_id="RetrieveUserAndActiveSubscriptionPlan",
        description="Retrieve a user and their active subscription plan.",
    ),
)
class UsersAndActiveSubscriptionPlansViewSet(CustomReadOnlyViewSet):
    """
    Users and active subscription plans viewset for Zedasignal Backend.
    """

    serializer_class = UserAndActiveSubscriptionPlanReadSerializer
    pagination_class = CustomPageNumberPagination
    lookup_field = "uuid"

    def get_object(self):
        user = get_object_or_404(User, uuid=self.request.query_params.get("uuid"))
        subscription_plan: SubscriptionPlan | None = user.subscriptions.filter(is_active=True).first()  # type: ignore

        return {
            "user": user,
            "subscription_plan": subscription_plan,
        }

    def get_queryset(self):
        users = User.objects.prefetch_related("subscriptions").filter(type=User.USER)

        users_and_active_subscription_plan_list = [
            {
                "id": index + 1,  # Increment id starting from 1
                "user": user,
                "subscription_plan": (
                    user.subscriptions.filter(is_active=True).first().plan  # type: ignore
                    if user.subscriptions.filter(is_active=True).exists()  # type: ignore
                    else None
                ),
            }
            for index, user in enumerate(users)  # Use enumerate to get the index
        ]

        return users_and_active_subscription_plan_list


class AdminActivateUserSubscription(APIView):
    """
    Activate user subscription view for Zedasignal Backend.
    """

    serializer_class = CreateUserSubscriptionSerializer

    @extend_schema(
        operation_id="ActivateUserSubscriptionPlan",
        responses={
            200: create_success_response_serializer(CreateUserSubscriptionSerializer()),
            400: ErrorResponseSerializer,
        },
        tags=["Trading"],
        description="Get activate user subscription plan.",
    )
    @admin_required
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return ErrorResponse(details=serializer.errors, status=400, message="Invalid data")
        subscription = serializer.save(created_by=request.user)
        domain = env.str("DOMAIN_NAME")
        Sender(
            subscription.user,
            email_content_object="notification.messages.subscription_activation",
            html_template="emails/trading/subscription/activation-notification.html",
            email_notif=True,
            context={
                "subscription_plan": subscription.plan,
                "subscription": subscription,
                "user": subscription.user,
                "domain": domain,
            },
        )

        return SuccessResponse(
            message="User subscription activated.",
        )
