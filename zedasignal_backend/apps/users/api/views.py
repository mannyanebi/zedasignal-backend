import environ
from django.conf import settings
from django_rest_passwordreset.serializers import (
    EmailSerializer,
    PasswordTokenSerializer,
)
from django_rest_passwordreset.views import (
    ResetPasswordConfirm,
    ResetPasswordRequestToken,
    ResetPasswordValidateToken,
    ResetTokenSerializer,
)
from djangorestframework_camel_case.parser import CamelCaseJSONParser
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.serializers import TokenBlacklistSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from zedasignal_backend.apps.users.models import VerificationCode
from zedasignal_backend.apps.users.utils import get_tokens_for_user
from zedasignal_backend.core.error_response import ErrorResponse
from zedasignal_backend.core.sender import Sender
from zedasignal_backend.core.success_response import SuccessResponse
from zedasignal_backend.core.utils.dict_to_object import DictToObject

from ..utils import get_custom_user_model
from .serializers import (
    ErrorResponseSerializer,
    SuccessResponseSerializer,
    UserCreateSerializer,
    UserLoginSerializer,
    UserSerializer,
    VerifyUserSerializer,
)

User = get_custom_user_model()
env = environ.Env()

HTTP_USER_AGENT_HEADER = getattr(
    settings, "DJANGO_REST_PASSWORDRESET_HTTP_USER_AGENT_HEADER", "HTTP_USER_AGENT"
)
HTTP_IP_ADDRESS_HEADER = getattr(
    settings, "DJANGO_REST_PASSWORDRESET_IP_ADDRESS_HEADER", "REMOTE_ADDR"
)


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    parser_classes = [CamelCaseJSONParser]
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)  # type: ignore # sanity check
        return self.queryset.filter(id=self.request.user.id)  # type: ignore

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return SuccessResponse(data=serializer.data, status=status.HTTP_200_OK)


class UserRegistrationView(APIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]
    throttle_scope = "high_critical_actions"

    @extend_schema(
        request=serializer_class,
        responses={
            201: OpenApiResponse(
                response=SuccessResponseSerializer,
                description="User registered successfully",
            ),
            400: ErrorResponseSerializer,
        },
        tags=["Auth"],
        description="Register a new technician",
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return SuccessResponse(
            message="User registered successfully",
            status=status.HTTP_201_CREATED,
        )


class VerifyUserAccount(APIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyUserSerializer
    throttle_scope = "low_critical_actions"

    @extend_schema(
        request=serializer_class,
        responses={200: SuccessResponseSerializer, 400: ErrorResponseSerializer},
        tags=["Auth"],
        description="Verify a user account",
    )
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]

        if len(code) != 6:
            return ErrorResponse(
                details="Invalid code format", status=status.HTTP_400_BAD_REQUEST
            )

        verification_codes = VerificationCode.objects.filter(email=email)

        if not verification_codes.exists():
            return ErrorResponse(
                details="Invalid verification code",
                status=status.HTTP_400_BAD_REQUEST,
            )
        verification_code = verification_codes.filter(code=code).first()
        # assert verification code is not none
        if verification_code is None:
            raise ValidationError("Invalid verification code")

        if verification_code.used:
            return ErrorResponse(
                details="Code already used", status=status.HTTP_400_BAD_REQUEST
            )

        # mark code as used
        verification_code.used = True
        verification_code.save(update_fields=["used"])

        other_user_verification_code = verification_codes.exclude(id=verification_code.id)  # type: ignore
        # delete all verification codes for this email
        other_user_verification_code.delete()

        return SuccessResponse(
            message="User account verified", status=status.HTTP_200_OK
        )


class SendVerificationCode(APIView):
    permission_classes = [AllowAny]
    serializer_class = EmailSerializer
    throttle_scope = "medium_critical_actions"

    @extend_schema(
        request=serializer_class,
        responses={200: SuccessResponseSerializer, 400: ErrorResponseSerializer},
        tags=["Auth"],
        description="Sends a verification code to a user",
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        verification_code = VerificationCode.objects.create(email=email)
        domain_name = env.str("DOMAIN_NAME")
        context = {
            "email": email,
            "verification_code": verification_code.code,
            "request_datetime": verification_code.created_at,
            "domain_name": domain_name,
        }
        user = DictToObject({"email": email})
        Sender(
            user,
            email_content_object="notification.messages.user_registration",
            html_template="emails/authentication/user-verification.html",
            email_notif=True,
            context=context,
        )

        return SuccessResponse(
            message="Verification code sent successfully", status=status.HTTP_200_OK
        )


class UserLoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    throttle_scope = "low_critical_actions"

    @extend_schema(
        request=serializer_class,
        responses={200: SuccessResponseSerializer, 400: ErrorResponseSerializer},
        tags=["Auth"],
        description="Login a user",
    )
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        if not serializer.is_valid():
            return ErrorResponse(
                details=serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        if not email or not password:
            return ErrorResponse(
                details="Username and password are required",
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.user_manager.get(username=email)
        except User.DoesNotExist:
            return ErrorResponse(
                details="User with email does not exist",
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.check_password(password):  # type: ignore
            return ErrorResponse(
                details="Invalid password",
                status=status.HTTP_400_BAD_REQUEST,
            )

        tokens = get_tokens_for_user(user)
        # include user object in response data
        user_data = UserSerializer(user).data
        response_data = {
            "user": user_data,
            "tokens": {**tokens},
        }

        return SuccessResponse(
            data=response_data, message="Login successful", status=status.HTTP_200_OK
        )


class UserLogoutView(APIView):
    """
    Logs out the user by invalidating their tokens.
    """

    @extend_schema(
        request=TokenBlacklistSerializer,
        responses={200: SuccessResponseSerializer, 400: ErrorResponseSerializer},
        tags=["Auth"],
        description="Logouts a user account. Expects a refresh token.",
    )
    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return ErrorResponse(
                details="Refresh token is required",
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  # Invalidate the refresh token

            return SuccessResponse(
                message="User successfully logged out",
                status=status.HTTP_205_RESET_CONTENT,
            )

        except Exception as e:  # noqa
            return ErrorResponse(
                details="Invalid refresh token",
                status=status.HTTP_400_BAD_REQUEST,
            )


class CustomResetPasswordRequestToken(APIView):
    serializer_class = EmailSerializer
    permission_classes = ()
    authentication_classes = ()
    throttle_scope = "medium_critical_actions"

    @extend_schema(
        request=EmailSerializer,
        responses={200: SuccessResponseSerializer, 400: ErrorResponseSerializer},
        tags=["Auth"],
        description="""An Api View which provides a method to request a password
        reset token based on an e-mail address. Sends a signal reset_password_token_created
        when a reset token was created""",
    )
    def post(self, request, *args, **kwargs):
        # Call the existing view
        reset_view = ResetPasswordRequestToken.as_view()
        response = reset_view(request=request._request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            return SuccessResponse(
                message="Password request token sent successfully",
                status=response.status_code,
                data=response.data,
            )
        else:
            error_data = response.data.get("error", [])
            if error_data:
                details = str(error_data[0].get("details"))
            else:
                details = "Check the request payload and try again"
            return ErrorResponse(
                message="Request for password reset token failed",
                details=details,
                status=response.status_code,
            )


class CustomResetPasswordConfirm(APIView):
    throttle_classes = ()
    permission_classes = ()
    serializer_class = PasswordTokenSerializer
    authentication_classes = ()
    throttle_scope = "low_critical_actions"

    @extend_schema(
        request=PasswordTokenSerializer,
        responses={200: SuccessResponseSerializer, 400: ErrorResponseSerializer},
        tags=["Auth"],
        description="An Api View which provides a method to reset a password based on a unique token.",
    )
    def post(self, request, *args, **kwargs):
        # Call the existing view
        reset_password_confirm_view = ResetPasswordConfirm.as_view()
        response = reset_password_confirm_view(
            request=request._request, *args, **kwargs
        )

        if response.status_code == status.HTTP_200_OK:
            return SuccessResponse(
                message="Password reset successfully",
                status=response.status_code,
                data=response.data,
            )
        else:
            error_data = response.data.get("error", [])
            if len(error_data) > 0:
                details = error_data
            else:
                details = "Check the request payload and try again"

            return ErrorResponse(
                message="Password reset failed",
                details=details,
                status=response.status_code,
            )


class CustomResetPasswordValidateToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    serializer_class = ResetTokenSerializer
    authentication_classes = ()
    throttle_scope = "low_critical_actions"

    @extend_schema(
        request=ResetTokenSerializer,
        responses={200: SuccessResponseSerializer, 400: ErrorResponseSerializer},
        tags=["Auth"],
        description="An Api View which provides a method to verify that a token is valid.",
    )
    def post(self, request, *args, **kwargs):
        # Call the existing view
        reset_password_validate_token_view = ResetPasswordValidateToken.as_view()
        response = reset_password_validate_token_view(
            request=request._request, *args, **kwargs
        )

        if response.status_code == status.HTTP_200_OK:
            return SuccessResponse(
                message="Password reset token validated successfully",
                status=response.status_code,
                data=response.data,
            )
        else:
            error_data = response.data.get("error", [])
            if error_data:
                details = str(error_data[0].get("details"))
            else:
                details = "Check the request payload and try again"
            return ErrorResponse(
                message="Password reset token validation failed",
                details=details,
                status=response.status_code,
            )
