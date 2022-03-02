from rest_framework import viewsets
from kvk.models import Kvk, Zerado
from mge.models import Inscrito, Mge, Punido, Ranking
from players.models import Alliance, Player, PlayerStatus

from api.serializers import (
    AllianceSerializer,
    InscritoSerializer,
    KvkSerializer,
    MgeSerializer,
    PlayerSerializer,
    PlayerSerializerForStaff,
    PlayerStatusSerializer,
    PunidoSerializer,
    RankingSerializer,
    ZeradoSerializer,
)


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return PlayerSerializerForStaff
        else:
            return PlayerSerializer


class AllianceViewSet(viewsets.ModelViewSet):
    queryset = Alliance.objects.all()
    serializer_class = AllianceSerializer


class PlayerStatusViewSet(viewsets.ModelViewSet):
    serializer_class = PlayerStatusSerializer

    def get_queryset(self):
        queryset = PlayerStatus.objects.all()
        if self.request.user.is_authenticated:
            return queryset.filter(player__game_id="29722921")
        else:
            return queryset.filter(player__game_id="29722921").order_by(
                "-data"
            )[:1]


class MgeViewSet(viewsets.ModelViewSet):
    queryset = Mge.objects.all()
    serializer_class = MgeSerializer


class PunidoViewSet(viewsets.ModelViewSet):
    queryset = Punido.objects.all()
    serializer_class = PunidoSerializer


class RankingViewSet(viewsets.ModelViewSet):
    queryset = Ranking.objects.all()
    serializer_class = RankingSerializer


class InscritoViewSet(viewsets.ModelViewSet):
    queryset = Inscrito.objects.all()
    serializer_class = InscritoSerializer


class KvkViewSet(viewsets.ModelViewSet):
    queryset = Kvk.objects.all()
    serializer_class = KvkSerializer


class ZeradoViewSet(viewsets.ModelViewSet):
    queryset = Zerado.objects.all()
    serializer_class = ZeradoSerializer
