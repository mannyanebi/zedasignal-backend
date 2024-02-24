from django.urls import path
from rest_framework.routers import SimpleRouter

from zedasignal_backend.apps.trading.views import SignalModelViewSet

router = SimpleRouter()

router.register("signals", SignalModelViewSet)
_urlpatterns = []
urlpatterns = router.urls + _urlpatterns
