from django.urls import path

from zedasignal_backend.apps.users.api.views import (
    CustomResetPasswordConfirm,
    CustomResetPasswordRequestToken,
    CustomResetPasswordValidateToken,
    SendVerificationCode,
    UserLoginView,
    UserLogoutView,
    UserRegistrationView,
    VerifyUserAccount,
)

# from rest_framework.routers import DefaultRouter, SimpleRouter


# if settings.DEBUG:
#     router = DefaultRouter()
# else:
#     router = SimpleRouter()

# router.register("users", UserViewSet)


_patterns = [
    path("register/", UserRegistrationView.as_view(), name="client-user-register"),  # type: ignore # noqa: E501
    path("verify/", VerifyUserAccount.as_view(), name="user-verification"),  # type: ignore
    path("send-verification-code/", SendVerificationCode.as_view(), name="user-verification-resend"),  # type: ignore # noqa: E501
    path("login/", UserLoginView.as_view(), name="user-login"),  # type: ignore
    path("logout/", UserLogoutView.as_view(), name="user-logout"),  # type: ignore
    path("password-reset/", CustomResetPasswordRequestToken.as_view(), name="reset-password-request"),  # type: ignore # noqa: E501
    path("password-reset/confirm/", CustomResetPasswordConfirm.as_view(), name="reset-password-confirm"),  # type: ignore # noqa: E501
    path("password-reset/validate-token/", CustomResetPasswordValidateToken.as_view(), name="reset-password-validate"),  # type: ignore # noqa: E501
]

app_name = "auth-api"
# urlpatterns = router.urls + _patterns
urlpatterns = _patterns
