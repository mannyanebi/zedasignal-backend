from drf_spectacular.utils import extend_schema, extend_schema_view
from zedasignal_backend.apps.education.models import AcademyVideo, Webinar
from zedasignal_backend.apps.education.serializers import (
    AcademyVideoSerializer,
    WebinarSerializer,
)
from zedasignal_backend.apps.users.api.serializers import (
    ErrorResponseSerializer,
    SuccessResponseSerializer,
)
from zedasignal_backend.core.views_mixins import CustomReadOnlyViewSet


# Create your views here.
@extend_schema_view(
    list=extend_schema(
        responses={200: SuccessResponseSerializer, 404: ErrorResponseSerializer},
        tags=["Academy Videos"],
        description="List all academy videos.",
    ),
    retrieve=extend_schema(
        responses={200: SuccessResponseSerializer, 404: ErrorResponseSerializer},
        tags=["Academy Videos"],
        description="Retrieve a academy video.",
    ),
)
class AcademyVideoModelViewSet(CustomReadOnlyViewSet):
    """
    Academy video model viewset for Zedasignal Backend.
    """

    serializer_class = AcademyVideoSerializer
    queryset = AcademyVideo.objects.all()
    lookup_field = "uuid"


@extend_schema_view(
    list=extend_schema(
        responses={200: SuccessResponseSerializer, 404: ErrorResponseSerializer},
        tags=["Webinars"],
        description="List all webinars.",
    ),
    retrieve=extend_schema(
        responses={200: SuccessResponseSerializer, 404: ErrorResponseSerializer},
        tags=["Webinars"],
        description="Retrieve a webinar.",
    ),
)
class WebinarModelViewSet(CustomReadOnlyViewSet):
    """
    Webinar model viewset for Zedasignal Backend.
    """

    serializer_class = WebinarSerializer
    queryset = Webinar.objects.all()
    lookup_field = "uuid"
