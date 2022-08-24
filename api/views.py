from datetime import datetime
from rest_framework import viewsets, filters
from django.db.models import Max

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
        return PlayerSerializer


class AllianceViewSet(viewsets.ModelViewSet):
    queryset = Alliance.objects.all()
    serializer_class = AllianceSerializer


class PlayerStatusViewSet(viewsets.ModelViewSet):
    queryset = PlayerStatus.objects.order_by("-data").all()
    serializer_class = PlayerStatusSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["=player__game_id"]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset

        max_date = self.queryset.aggregate(Max("data"))
        apenas_dia = str(max_date["data__max"])
        apenas_dia = datetime.fromisoformat(apenas_dia)
        apenas_dia = apenas_dia.replace(hour=0, minute=0, second=0)
        queryset = self.queryset.filter(data__gte=apenas_dia)
        return queryset


class Top10PowerViewSet(viewsets.ModelViewSet):
    queryset = PlayerStatus.objects.order_by("-data").all()
    serializer_class = PlayerStatusSerializer

    def get_queryset(self):
        ultimo = PlayerStatus.objects.order_by("-data").first()

        o_reino_poder = (
            PlayerStatus.objects.exclude(player__alliance__tag="MIGR")
            .exclude(player__status="INATIVO")
            .exclude(player__status="BANIDO")
            .filter(
                data__year=ultimo.data.year,
                data__month=ultimo.data.month,
                data__day=ultimo.data.day,
            )
            .order_by("-power")
        )

        return o_reino_poder[:10]


class Top10KillPointsViewSet(viewsets.ModelViewSet):
    queryset = PlayerStatus.objects.order_by("-data").all()
    serializer_class = PlayerStatusSerializer

    def get_queryset(self):
        ultimo = PlayerStatus.objects.order_by("-data").first()

        o_reino_killpoints = (
            PlayerStatus.objects.exclude(player__alliance__tag="MIGR")
            .exclude(player__status="INATIVO")
            .exclude(player__status="BANIDO")
            .filter(
                data__year=ultimo.data.year,
                data__month=ultimo.data.month,
                data__day=ultimo.data.day,
            )
            .order_by("-killpoints")
        )

        return o_reino_killpoints[:10]


class Top10MortesViewSet(viewsets.ModelViewSet):
    queryset = PlayerStatus.objects.order_by("-data").all()
    serializer_class = PlayerStatusSerializer

    def get_queryset(self):
        ultimo = PlayerStatus.objects.order_by("-data").first()

        o_reino_mortes = (
            PlayerStatus.objects.exclude(player__alliance__tag="MIGR")
            .exclude(player__status="INATIVO")
            .exclude(player__status="BANIDO")
            .filter(
                data__year=ultimo.data.year,
                data__month=ultimo.data.month,
                data__day=ultimo.data.day,
            )
            .order_by("-deaths")
        )

        return o_reino_mortes[:10]


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
