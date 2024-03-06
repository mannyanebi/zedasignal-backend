from typing import TypeVar

from django.conf import settings
from django.contrib.auth.password_validation import get_password_validators, validate_password
from drf_spectacular.utils import inline_serializer
from rest_framework import serializers

from zedasignal_backend.apps.users.models import Profile
from zedasignal_backend.apps.users.types import UserType

# from django.contrib.auth import get_user_model
from zedasignal_backend.apps.users.utils import get_custom_user_model

User = get_custom_user_model()

T = TypeVar("T", bound="serializers.Serializer")


class UserFullNameField(serializers.CharField):
    def to_internal_value(self, data):
        # Split the incoming full name into first name and last name
        if type(data) is str:
            names = data.split()
            if len(names) > 1:
                return {
                    "first_name": names[0],
                    "last_name": " ".join(names[1:]),
                }
            else:
                return {
                    "first_name": names[0],
                    "last_name": "",
                }
        return data

    def to_representation(self, obj):
        # Combine first name and last name into full name during serialization
        return f"{obj['first_name']} {obj['last_name']}"


class PasswordField(serializers.CharField):
    def to_internal_value(self, data):
        # Validate the password using Django's validators
        validate_password(
            data,
            password_validators=get_password_validators(settings.AUTH_PASSWORD_VALIDATORS),
        )
        return data


class UserSerializer(serializers.ModelSerializer[UserType | User]):
    class Meta:
        model = User
        exclude = (
            "password",
            "is_staff",
            "is_active",
            "date_joined",
            "is_superuser",
            "groups",
            "user_permissions",
            "last_login",
            "id",
        )

        # extra_kwargs = {
        #     "url": {"view_name": "users:detail", "lookup_field": "username"},
        # }


class UserCreateSerializer(serializers.ModelSerializer[UserType]):
    password = PasswordField(write_only=True)
    full_name = UserFullNameField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ("email", "password", "phone_number", "full_name")

        extra_kwargs = {
            "username": {"required": False},
        }

    def create(self, validated_data):
        # Handle full_name field and convert it to first_name and last_name
        full_name = validated_data.pop("full_name", None)
        if full_name:
            validated_data["first_name"] = full_name.get("first_name", "")
            validated_data["last_name"] = full_name.get("last_name", "")

        user = User.user_manager.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            username=validated_data.get("username", None),
            phone_number=validated_data.get("phone_number", ""),
        )

        return user


class UserProfileCreateSerializer(serializers.ModelSerializer[Profile]):
    class Meta:
        model = Profile
        fields = (
            "has_trading_experience",
            "ref_id",
            "amount_range_to_trade_with",
        )

    def create(self, validated_data):
        profile = Profile.objects.create(**validated_data)
        return profile


class UserProfileReadSerializer(serializers.ModelSerializer[Profile]):
    class Meta:
        model = Profile
        exclude = ("id", "user")


class UserUpdateSerializer(serializers.ModelSerializer[UserType]):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone_number",
        )

        extra_kwargs = {
            "first_name": {"required": False},
            "last_name": {"required": False},
        }


class VerifyUserSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    code = serializers.CharField(max_length=6)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(min_length=8, required=True)


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class SuccessResponseSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=255)
    success = serializers.BooleanField(default=True)
    result = serializers.DictField(child=serializers.CharField(), allow_empty=True, read_only=True)


class ErrorResponseChildSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=20)
    message = serializers.CharField(max_length=255)
    details = serializers.CharField(max_length=255)


class ErrorResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=False)
    error = serializers.ListField(child=ErrorResponseChildSerializer())


def create_success_response_serializer(
    result_serializer: T,
) -> serializers.Serializer[T]:
    """
    Dynamically create a SuccessResponseSerializer with a result field
    that uses the provided result_serializer.
    """
    # Use __class__.__name__ to get the name of the class of the result_serializer instance
    serializer_class_name = result_serializer.__class__.__name__
    return inline_serializer(
        name=f"DynamicSuccessResponseSerializer{serializer_class_name}",
        fields={
            "message": serializers.CharField(),
            "success": serializers.BooleanField(default=True),
            "result": result_serializer,
        },
    )


# class TechnicianReadSerializer(serializers.ModelSerializer[Technician]):
#     user = UserSerializer()

#     class Meta:
#         model = Technician
#         exclude = ["is_deleted", "id"]


# class TechnicianTypeSerializer(serializers.ModelSerializer[TechnicianType]):
#     class Meta:
#         model = TechnicianType
#         exclude = ["id"]


# class TechniciansResponseCountChildSerializer(serializers.Serializer):
#     count = serializers.IntegerField()
#     result = TechnicianReadSerializer(many=True)


# class TechniciansResponseCountSerializer(SuccessResponseSerializer):
#     result = TechniciansResponseCountChildSerializer()
