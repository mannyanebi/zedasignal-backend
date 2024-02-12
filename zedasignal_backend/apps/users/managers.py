from typing import Any

from django.contrib.auth.models import BaseUserManager
from django.db.models.query import QuerySet
from django.db.utils import IntegrityError

from zedasignal_backend.apps.users.types import UserType


class CustomUserManager(BaseUserManager):
    def get(self, *args: Any, **kwargs: Any) -> UserType:
        return super().get(*args, **kwargs)

    def create(self, *args: Any, **kwargs: Any) -> UserType:
        return super().create(*args, **kwargs)

    def filter(self, *args: Any, **kwargs: Any) -> QuerySet[UserType]:
        return super().filter(*args, **kwargs)

    def create_user(
        self, email, username=None, password=None, **extra_fields
    ) -> UserType:
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        if username == "":
            raise ValueError("The Username field cannot be an empty string")

        username_value = username if username is not None else email
        user = self.model(email=email, username=username_value, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user_with_phone(
        self, phone_number, username, password=None, **extra_fields
    ) -> UserType:
        if not phone_number:
            raise ValueError("The Phone Number field must be set")

        try:
            username_value = username if username is not None or "" else phone_number
            user = self.model(
                phone_number=phone_number, username=username_value, **extra_fields
            )
            user.set_password(password)
            user.save(using=self._db)
            return user
        except IntegrityError:
            raise ValueError("Username or phone number is already in use")

    def create_superuser(self, username, password=None, **extra_fields) -> UserType:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        email = username
        return self.create_user(email, username, password, **extra_fields)
