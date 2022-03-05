from rest_framework import viewsets, filters
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
    filter_backends = [filters.SearchFilter]
    search_fields = ["=game_id", "nick"]

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return PlayerSerializerForStaff
        else:
            return PlayerSerializer


class AllianceViewSet(viewsets.ModelViewSet):
    queryset = Alliance.objects.all()
    serializer_class = AllianceSerializer


class PlayerStatusViewSet(viewsets.ModelViewSet):
    queryset = PlayerStatus.objects.all()
    serializer_class = PlayerStatusSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["=player__game_id"]


class MgeViewSet(viewsets.ModelViewSet):
    queryset = Mge.objects.all()
    serializer_class = MgeSerializer


class PunidoViewSet(viewsets.ModelViewSet):
    queryset = Punido.objects.all()
    serializer_class = PunidoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["=mge__id"]


class RankingViewSet(viewsets.ModelViewSet):
    queryset = Ranking.objects.all()
    serializer_class = RankingSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["=mge__id"]


class InscritoViewSet(viewsets.ModelViewSet):
    queryset = Inscrito.objects.all()
    serializer_class = InscritoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["=mge__id"]


class KvkViewSet(viewsets.ModelViewSet):
    queryset = Kvk.objects.all()
    serializer_class = KvkSerializer


class ZeradoViewSet(viewsets.ModelViewSet):
    queryset = Zerado.objects.all()
    serializer_class = ZeradoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["=kvk__id"]
