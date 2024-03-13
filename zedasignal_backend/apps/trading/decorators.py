from rest_framework import status

from zedasignal_backend.apps.users.utils import get_custom_user_model
from zedasignal_backend.core.error_response import ErrorResponse

User = get_custom_user_model()


def user_has_active_subscription(function=None):
    """
    Decorator for views that checks that the logged in user has
     an active subscription, else returns a 403
    """

    user_is_subscribed = lambda user: user.subscriptions.filter(is_active=True).exists()  # type: ignore # noqa: E731, E501

    def _wrapped_view(self, request, *args, **kwargs):
        if user_is_subscribed(request.user):
            if function:
                return function(self, request, *args, **kwargs)
        else:
            return ErrorResponse(
                details="You are not authorized to access this resource",
                status=status.HTTP_403_FORBIDDEN,
            )

    if function:
        return _wrapped_view

    return user_is_subscribed


def user_has_active_subscription_or_is_admin(function=None):
    """
    Decorator for views that checks that the logged in user has
     an active subscription or is an admin, else returns a 403
    """

    user_is_subscribed = lambda user: user.subscriptions.filter(is_active=True).exists()  # type: ignore # noqa: E731, E501

    def _wrapped_view(self, request, *args, **kwargs):
        if user_is_subscribed(request.user) or request.user.type == User.ADMIN:
            if function:
                return function(self, request, *args, **kwargs)
        else:
            return ErrorResponse(
                details="You are not authorized to access this resource",
                status=status.HTTP_403_FORBIDDEN,
            )

    if function:
        return _wrapped_view

    return user_is_subscribed
