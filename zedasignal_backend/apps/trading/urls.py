from django.urls import path
from rest_framework.routers import SimpleRouter

from zedasignal_backend.apps.trading.views import (
    AdminActivateUserSubscription,
    AdminCreateSignal,
    AdminDashboardStatisticsView,
    SignalModelViewSet,
    SubscriptionPlanViewSet,
    UserActiveSubscriptionPlans,
    UsersAndActiveSubscriptionPlansViewSet,
)

router = SimpleRouter()

router.register("signals", SignalModelViewSet, basename="signals")
router.register("subscription-plans", SubscriptionPlanViewSet, basename="subscription-plans")
router.register(
    "users-and-active-subscription-plans",
    UsersAndActiveSubscriptionPlansViewSet,
    basename="users-and-active-subscription-plans",
)
_urlpatterns = [
    path(
        "user-active-subscription-plans/",
        UserActiveSubscriptionPlans.as_view(),  # type: ignore
        name="user-active-subscription-plans",
    ),  # noqa
    path("create-signal/", AdminCreateSignal.as_view(), name="create-signal"),  # type: ignore
    path(
        "activate-user-subscription-plan/",
        AdminActivateUserSubscription.as_view(),  # type: ignore
        name="activate-user-subscription-plan",
    ),  # type: ignore
    path(
        "admin-dashboard-statistics/",
        AdminDashboardStatisticsView.as_view(),  # type: ignore
        name="admin-dashboard-statistics",
    ),
]
urlpatterns = router.urls + _urlpatterns
