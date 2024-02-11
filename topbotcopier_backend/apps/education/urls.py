from rest_framework.routers import SimpleRouter

from zedasignal_backend.apps.education.views import (
    AcademyVideoModelViewSet,
    WebinarModelViewSet,
)

router = SimpleRouter()

router.register("webinar", WebinarModelViewSet)
router.register("academy-video", AcademyVideoModelViewSet)


urlpatterns = router.urls
