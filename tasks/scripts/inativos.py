from players.models import Player, PlayerStatus


def main() -> str:
    ultima_leitura = PlayerStatus.objects.all().order_by("-data").first().data

    ativos_no_top500 = PlayerStatus.objects.filter(
        data__year=ultima_leitura.year,
        data__month=ultima_leitura.month,
        data__day=ultima_leitura.day,
    )

    game_ids_ativos = [status.player.game_id for status in ativos_no_top500]

    nao_mudar = ["MIGROU", "BANIDO", "INATIVO"]

    players = (
        Player.objects.exclude(game_id__in=game_ids_ativos)
        .exclude(status__in=nao_mudar)
        .update(status="INATIVO")
    )

    return f"Atualizados os status de {players} player(s)."
