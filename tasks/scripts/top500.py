from django import forms
from players.models import Player, PlayerStatus
from tasks.scripts.script import RiseTask, RiseTaskResponse


class Top500Task(RiseTask):
    def run(self) -> RiseTaskResponse:
        ultima_leitura = (
            PlayerStatus.objects.all().order_by("-data").first().data
        )

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

        response = RiseTaskResponse(
            f"Atualizados os status de {players} player(s)."
        )

        return response

    def render(self) -> forms.BaseForm:
        return None


def main() -> RiseTask:
    return Top500Task(
        nome="Top 500",
        descricao="Torna todos os inativos e que \
                           migraram e voltaram a aparecer na última leitura em player.",
    )
