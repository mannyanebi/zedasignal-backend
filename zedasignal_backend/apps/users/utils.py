# from typing import Dict

from rest_framework_simplejwt.tokens import RefreshToken, Token, TokenError

from zedasignal_backend.apps.users.models import User
from zedasignal_backend.apps.users.types import UserType


def get_custom_user_model():
    """
    Returns:
        User: Custom user model defined in users app.
    """
    return User


def generate_token_for_user(user):
    token = Token.for_user(user)
    return {
        "token": str(token),
    }


def get_user_from_token(token):
    try:
        return Token(token).get("user")
    except TokenError as e:
        raise TokenError(f"Invalid token: {e}")


def get_tokens_for_user(user: UserType) -> dict[str, str]:
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
