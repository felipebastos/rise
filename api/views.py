from rest_framework import filters, viewsets

from api.serializers import AllianceSerializer, PlayerSerializer, PlayerStatusSerializer
from players.models import Alliance, Player, PlayerStatus


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class AllianceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Alliance.objects.all()
    serializer_class = AllianceSerializer


class PlayerStatusViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PlayerStatusSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["power", "killpoints", "deaths"]
    ordering = ["-power"]

    def get_queryset(self):
        ultimo = PlayerStatus.objects.order_by("-data").first()

        o_reino = (
            PlayerStatus.objects.exclude(player__alliance__tag="MIGR")
            .exclude(player__status="INATIVO")
            .exclude(player__status="BANIDO")
            .filter(
                data__year=ultimo.data.year,
                data__month=ultimo.data.month,
                data__day=ultimo.data.day,
            )
        )

        return o_reino
