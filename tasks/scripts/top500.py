from players.models import Player, PlayerStatus


def main() -> str:
    ultima_leitura = PlayerStatus.objects.all().order_by("-data").first().data

    ativos_no_top500 = PlayerStatus.objects.filter(
        data__year=ultima_leitura.year,
        data__month=ultima_leitura.month,
        data__day=ultima_leitura.day,
    )

    game_ids_ativos = [status.player.game_id for status in ativos_no_top500]

    mudar = ["MIGROU", "INATIVO"]

    players = (
        Player.objects.filter(game_id__in=game_ids_ativos)
        .filter(status__in=mudar)
        .update(status="PLAYER")
    )

    return f"Atualizados os status de {players} player(s)."
