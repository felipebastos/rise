from django.db.models import Max, Min

from kvk.models import Batalha, Kvk
from players.models import PlayerStatus


def get_kvk_ranking(kvk: Kvk):
    data = {}
    for batalha in Batalha.objects.filter(kvk=kvk):
        in_battle_data = (
            PlayerStatus.objects.filter(
                data__gte=batalha.data_inicio, data__lte=batalha.data_fim
            )
            .values("player__game_id", "player__nick")
            .annotate(
                kp=Max("killpoints") - Min("killpoints"),
                dt=Max("deaths") - Min("deaths"),
            )
        )
    return sorted(ranking.items(), key=lambda x: x[1], reverse=True)
