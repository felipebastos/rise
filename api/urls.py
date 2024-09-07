from django.urls import include, path
from rest_framework import routers

from api.views import AllianceViewSet, PlayerStatusViewSet, PlayerViewSet

router = routers.DefaultRouter()
router.register(r"players", PlayerViewSet)
router.register(r"alliances", AllianceViewSet)
router.register(r"playerstatus", PlayerStatusViewSet, basename="playerstatus")

urlpatterns = [
    path("", include(router.urls)),
]
