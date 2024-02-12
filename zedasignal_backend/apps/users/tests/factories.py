from collections.abc import Sequence
from typing import Any

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from factory import Faker, post_generation
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    username = Faker("user_name")
    email = Faker("email")
    name = Faker("name")

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={"locale": None})
        )
        self.set_password(password)

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]


class BaseTestCase(TestCase):
    def get_authorization_token(self):
        # Login and get access token
        client_data = {"username": self.username, "password": "polymarq"}
        url = reverse("auth-api:user-login")
        response = self.client.post(url, client_data, content_type="application/json").json()
        return response["result"]["access"]

    @property
    def headers(self):
        # Set authorization credentials
        token = self.get_authorization_token()
        headers = {"Authorization": f"Bearer {token}", "content_type": "application/json"}
        return headers
