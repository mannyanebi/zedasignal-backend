import environ
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.views import APIView
from zedasignal_backend.apps.trading.models import (
    AccountScreeningRequest,
    Bot,
    BotlabBot,
    CopyTradingGuide,
    SubscriptionPlan,
    TopPerformingBot,
)
from zedasignal_backend.apps.trading.serializers import (
    AccountScreeningRequestSerializer,
    BotlabBotSerializer,
    BotSerializer,
    CopyTradingGuideSerializer,
    CreateAccountUpgradePaymentRequestSerializer,
    HelpSupportRequestSerializer,
    ReadAccountUpgradePaymentRequestSerializer,
    SubscriptionPlanSerializer,
    TopPerformingBotSerializer,
)
from zedasignal_backend.apps.users.api.serializers import (
    ErrorResponseSerializer,
    SuccessResponseSerializer,
)
from zedasignal_backend.core.error_response import ErrorResponse
from zedasignal_backend.core.sender import Sender
from zedasignal_backend.core.success_response import SuccessResponse
from zedasignal_backend.core.utils.dict_to_object import DictToObject
from zedasignal_backend.core.views_mixins import CustomReadOnlyViewSet

env = environ.Env()


# Create your views here.
@extend_schema_view(
    list=extend_schema(
        responses={200: SuccessResponseSerializer, 404: ErrorResponseSerializer},
        tags=["Bots"],
        description="List all bots.",
    ),
    retrieve=extend_schema(
        responses={200: SuccessResponseSerializer, 404: ErrorResponseSerializer},
        tags=["Bots"],
        description="Retrieve a bot.",
    ),
)
class BotModelViewSet(CustomReadOnlyViewSet):
    """
    Bot model viewset for Zedasignal Backend.
    """

    serializer_class = BotSerializer
    queryset = Bot.objects.filter(is_active=True)
    lookup_field = "uuid"


@extend_schema_view(
    list=extend_schema(
        responses={200: SuccessResponseSerializer, 404: ErrorResponseSerializer},
        tags=["Top Performing Bots"],
        description="List all top performing bots.",
    ),
    retrieve=extend_schema(
        responses={200: SuccessResponseSerializer, 404: ErrorResponseSerializer},
        tags=["Top Performing Bots"],
        description="Retrieve a top performing bot.",
    ),
)
class TopPerformingBotModelViewSet(CustomReadOnlyViewSet):
    """
    Top Performing Bot model viewset for Zedasignal Backend.
    """

    serializer_class = TopPerformingBotSerializer
    queryset = TopPerformingBot.objects.all()
    lookup_field = "uuid"


@extend_schema_view(
    list=extend_schema(
        responses={200: SuccessResponseSerializer, 404: ErrorResponseSerializer},
        tags=["Subscription Plans"],
        description="List all subscription plans.",
    ),
    retrieve=extend_schema(
        responses={200: SuccessResponseSerializer, 404: ErrorResponseSerializer},
        tags=["Subscription Plans"],
        description="Retrieve a subscription plan.",
    ),
)
class SubscriptionPlanModelViewSet(CustomReadOnlyViewSet):
    """
    Subscription plan model viewset for Zedasignal Backend.
    """

    serializer_class = SubscriptionPlanSerializer
    queryset = SubscriptionPlan.objects.prefetch_related("promos").filter(
        is_active=True
    )
    lookup_field = "uuid"


@extend_schema_view(
    list=extend_schema(
        responses={200: SuccessResponseSerializer, 404: ErrorResponseSerializer},
        tags=["Copy Trading Guides"],
        description="List all copy trading guides.",
    ),
    retrieve=extend_schema(
        responses={200: SuccessResponseSerializer, 404: ErrorResponseSerializer},
        tags=["Copy Trading Guides"],
        description="Retrieve a copy trading guide.",
    ),
)
class CopyTradingGuideModelViewSet(CustomReadOnlyViewSet):
    """
    Subscription plan model viewset for Zedasignal Backend.
    """

    serializer_class = CopyTradingGuideSerializer
    queryset = CopyTradingGuide.objects.all()
    lookup_field = "bot__uuid"


class CreateAccountScreeningRequestView(APIView):
    """
    Create account screening request view for Zedasignal Backend.
    """

    serializer_class = AccountScreeningRequestSerializer
    throttle_scope = "user_account_request_actions"

    @extend_schema(
        request=serializer_class,
        responses={200: SuccessResponseSerializer, 400: ErrorResponseSerializer},
        tags=["Account Screening Requests"],
        description="Create account screening request.",
    )
    def post(self, request):
        """
        Create account screening request.
        """
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        domain_name = env.str("DOMAIN_NAME")

        support_user = DictToObject(
            {
                "email": "support@zedasignal.com",
            }
        )

        context = {"domain_name": domain_name, **serializer.data}

        Sender(
            support_user,
            email_content_object="notification.messages.account_screening_request",
            html_template="emails/account-screening-request/notification.html",
            email_notif=True,
            context=context,
        )

        return SuccessResponse(message="Request successful", status=status.HTTP_200_OK)


class CheckAccountScreeningRequestApprovalView(APIView):
    """
    Check account screening request approval view for Zedasignal Backend.
    """

    @extend_schema(
        responses={200: SuccessResponseSerializer, 400: ErrorResponseSerializer},
        tags=["Account Screening Requests"],
        description="Check account screening request approval.",
    )
    def get(self, request):
        """
        Check account screening request approval.
        """
        user = request.user
        account_screening_request_qs = AccountScreeningRequest.objects.filter(user=user)

        if not account_screening_request_qs.exists():
            return ErrorResponse(
                details="No account screening found. Please initiate an account screening request to proceed.",
                status=status.HTTP_404_NOT_FOUND,
            )

        account_screening_request_approved_qs = account_screening_request_qs.filter(
            is_approved=True
        )

        if not account_screening_request_approved_qs.exists():
            return ErrorResponse(
                details="Account screening is not yet approved.",
                status=status.HTTP_404_NOT_FOUND,
            )

        return SuccessResponse(
            message="Request successful",
            status=status.HTTP_200_OK,
            data={"is_approved": True},
        )


class HelpSupportRequestView(APIView):
    """
    Help support request view for Zedasignal Backend.
    """

    serializer_class = HelpSupportRequestSerializer
    throttle_scope = "user_account_request_actions"

    @extend_schema(
        request=serializer_class,
        responses={200: SuccessResponseSerializer, 400: ErrorResponseSerializer},
        tags=["Help Support Requests"],
        description="Create help support request.",
    )
    def post(self, request):
        """
        Create help support request.
        """
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        domain_name = env.str("DOMAIN_NAME")

        support_user = DictToObject(
            {
                "email": "support@zedasignal.com",
            }zedasignal
        )

        context = {"domain_name": domain_name, "user": user, **serializer.data}

        Sender(
            support_user,
            email_content_object="notification.messages.help_support_request",
            html_template="emails/help-support-request/notification.html",
            email_notif=True,
            context=context,
        )

        return SuccessResponse(message="Request successful", status=status.HTTP_200_OK)


@extend_schema_view(
    list=extend_schema(
        responses={200: SuccessResponseSerializer, 404: ErrorResponseSerializer},
        tags=["Botlab Bots"],
        description="List all botlab bots.",
    ),
    retrieve=extend_schema(
        responses={200: SuccessResponseSerializer, 404: ErrorResponseSerializer},
        tags=["Botlab Bots"],
        description="Retrieve a botlab bot.",
    ),
)
class BotlabBotsModelViewSet(CustomReadOnlyViewSet):
    """
    Botlab bots model viewset for Zedasignal Backend.
    """

    serializer_class = BotlabBotSerializer
    queryset = BotlabBot.objects.filter(is_delisted=False)
    lookup_field = "uuid"


class CreateAccountUpgradePaymentRequestView(APIView):
    """
    Create account upgrade payment request view for Zedasignal Backend.
    """

    serializer_class = CreateAccountUpgradePaymentRequestSerializer
    throttle_scope = "user_account_request_actions"

    @extend_schema(
        request=serializer_class,
        responses={200: SuccessResponseSerializer, 400: ErrorResponseSerializer},
        tags=["Account Upgrade Payment Requests"],
        description="Create account upgrade payment request.",
    )
    def post(self, request):
        """
        Create account upgrade payment request.
        """
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        account_upgrade_payment_request = serializer.save(user=user)
        domain_name = env.str("DOMAIN_NAME")

        support_user = DictToObject(
            {
                "email": "support@zedasignal.com",
            }
        )

        account_upgrade_payment_request_dict = (
            ReadAccountUpgradePaymentRequestSerializer(
                account_upgrade_payment_request
            ).data
        )

        context = {"domain_name": domain_name, **account_upgrade_payment_request_dict}
        context.update({"created_at": account_upgrade_payment_request.created_at})

        Sender(
            support_user,
            email_content_object="notification.messages.account_upgrade_payment_request",
            html_template="emails/account-upgrade-payment-request/notification.html",
            email_notif=True,
            context=context,
        )

        return SuccessResponse(message="Request successful", status=status.HTTP_200_OK)
