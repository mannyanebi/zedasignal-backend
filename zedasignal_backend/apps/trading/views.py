from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from zedasignal_backend.apps.trading.models import Signal, SubscriptionPlan
from zedasignal_backend.apps.trading.serializers import (
    SignalCreateSerializer,
    SignalReadSerializer,
    SubscriptionPlanReadSerializer,
    UserActiveSubscriptionPlanReadSerializer,
)
from zedasignal_backend.apps.users.api.serializers import ErrorResponseSerializer, create_success_response_serializer
from zedasignal_backend.core.error_response import ErrorResponse
from zedasignal_backend.core.success_response import SuccessResponse
from zedasignal_backend.core.views_mixins import CustomReadOnlyViewSet


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
    queryset = SubscriptionPlan.objects.filter(is_active=True)
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
