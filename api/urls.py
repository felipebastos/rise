from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from api.views import (
    AllianceViewSet,
    InscritoViewSet,
    KvkViewSet,
    MgeViewSet,
    PlayerStatusViewSet,
    PlayerViewSet,
    PunidoViewSet,
    RankingViewSet,
    Top10KillPointsViewSet,
    Top10MortesViewSet,
    Top10PowerViewSet,
    ZeradoViewSet,
)

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r"players", PlayerViewSet)
router.register(r"alliances", AllianceViewSet)
router.register(
    r"playerstatuses", PlayerStatusViewSet, basename="playerstatuses"
)
router.register(r"mges", MgeViewSet)
router.register(r"punidos", PunidoViewSet)
router.register(r"rankings", RankingViewSet)
router.register(r"inscritos", InscritoViewSet)
router.register(r"kvks", KvkViewSet)
router.register(r"zerados", ZeradoViewSet)
router.register(r"power", Top10PowerViewSet)
router.register(r"killpoints", Top10KillPointsViewSet)
router.register(r"deaths", Top10MortesViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
