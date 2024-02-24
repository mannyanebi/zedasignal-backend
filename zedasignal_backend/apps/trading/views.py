from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework.views import APIView

from zedasignal_backend.apps.trading.models import Signal
from zedasignal_backend.apps.trading.serializers import SignalReadSerializer
from zedasignal_backend.apps.users.api.serializers import (
    ErrorResponseSerializer,
    SuccessResponseSerializer,
    create_success_response_serializer,
)
from zedasignal_backend.core.views_mixins import CustomReadOnlyViewSet

# Create your views here.
# class AdminCreateSignal(APIView):


#     @extend_schema(
#         request=serializer_class,
#         responses={
#             200: create_success_response_serializer(UserSerializer()),
#             400: ErrorResponseSerializer,
#         },
#         tags=["Signals"],
#         description="",
#     )


@extend_schema_view(
    list=extend_schema(
        responses={
            200: create_success_response_serializer(SignalReadSerializer()),
            404: ErrorResponseSerializer,
        },
        tags=["Signals"],
        operation_id="ListSignals",
        description="List all signals.",
    ),
    retrieve=extend_schema(
        responses={
            200: create_success_response_serializer(SignalReadSerializer()),
            404: ErrorResponseSerializer,
        },
        tags=["Signals"],
        operation_id="RetrieveSignal",
        description="Retrieve a signal.",
    ),
)
class SignalModelViewSet(CustomReadOnlyViewSet):
    """
    Signal model viewset for Zedasignal Backend.
    """

    serializer_class = SignalReadSerializer
    queryset = Signal.objects.filter(is_active=True)
    lookup_field = "uuid"
