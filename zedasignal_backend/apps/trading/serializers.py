from rest_framework import serializers

from zedasignal_backend.apps.users.api.serializers import UserSerializer

from .models import Signal


class SignalReadSerializer(serializers.ModelSerializer[Signal]):
    author = UserSerializer()

    class Meta:
        model = Signal
        exclude = ("id",)
