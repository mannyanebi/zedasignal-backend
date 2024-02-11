from django.urls import path
from rest_framework.routers import SimpleRouter

from zedasignal_backend.apps.trading.views import (
    BotlabBotsModelViewSet,
    BotModelViewSet,
    CheckAccountScreeningRequestApprovalView,
    CopyTradingGuideModelViewSet,
    CreateAccountScreeningRequestView,
    CreateAccountUpgradePaymentRequestView,
    HelpSupportRequestView,
    SubscriptionPlanModelViewSet,
    TopPerformingBotModelViewSet,
)

router = SimpleRouter()

router.register("bots", BotModelViewSet)
router.register("subscription-plans", SubscriptionPlanModelViewSet)
router.register("copy-trading-guide", CopyTradingGuideModelViewSet)
router.register("top-performing-bots", TopPerformingBotModelViewSet)
router.register("bot-lab-bots", BotlabBotsModelViewSet)

_urlpatterns = [
    path("account-screening-request/", CreateAccountScreeningRequestView.as_view(), name="account-screening-request"),  # type: ignore # noqa: E501
    path("check-account-screening-request-approval/", CheckAccountScreeningRequestApprovalView.as_view(), name="check-account-screening-request-approval"),  # type: ignore # noqa: E501
    path("help-support-request/", HelpSupportRequestView.as_view(), name="help-support-request"),  # type: ignore # noqa: E501
    path("account-upgrade-payment-request/", CreateAccountUpgradePaymentRequestView.as_view(), name="account-upgrade-payment-request"),  # type: ignore # noqa: E501
]

urlpatterns = router.urls + _urlpatterns
