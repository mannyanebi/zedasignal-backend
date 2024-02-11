from typing import Any

from rest_framework import mixins
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from zedasignal_backend.core.success_response import SuccessResponse


class CustomReadOnlyViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        response = super().list(request, *args, **kwargs)
        return SuccessResponse(
            status=response.status_code,
            data=response.data,
        )

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        response = super().retrieve(request, *args, **kwargs)
        return SuccessResponse(
            status=response.status_code,
            data=response.data,
        )
