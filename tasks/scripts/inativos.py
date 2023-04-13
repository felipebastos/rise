from django import forms

from players.models import Player, PlayerStatus
from tasks.scripts.script import RiseTask, RiseTaskResponse


class InativosTask(RiseTask):
    def run(self, from_form: forms.Form = None) -> RiseTaskResponse:
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

        response = RiseTaskResponse(f"Atualizados os status de {players} player(s).")
        return response

    def render(self) -> forms.BaseForm:
        return None


def main() -> RiseTask:
    return InativosTask(
        nome="Atualiza inativos da última leitura",
        descricao="Todos os jogadores que não estão na última leitura e não \
                            são banidos ou que já migraram, terão o status mudado para inativo.",
    )
