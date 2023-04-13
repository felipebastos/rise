from typing import Type

from django import forms

from players.models import Player, PlayerStatus
from tasks.scripts.script import RiseTask, RiseTaskResponse


class Top500TaskForm(forms.Form):
    limite = forms.IntegerField(
        label="Limite máximo",
        max_value=1000,
        min_value=0,
        initial=500,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "title": "Maior posição em que o script atuará.",
            }
        ),
    )


class Top500Task(RiseTask):
    def run(self, from_form: forms.Form = None) -> RiseTaskResponse:
        ultima_leitura = PlayerStatus.objects.all().order_by("-data").first().data

        ativos_no_top500 = None

        if from_form.is_valid():
            ativos_no_top500 = PlayerStatus.objects.filter(
                data__year=ultima_leitura.year,
                data__month=ultima_leitura.month,
                data__day=ultima_leitura.day,
            ).order_by("data")[: from_form.cleaned_data.get("limite")]
        else:
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
            .update(status="VIGIAR")
        )

        response = RiseTaskResponse(f"Atualizados os status de {players} player(s).")

        return response

    def form_class(self) -> Type[forms.Form]:
        return Top500TaskForm


def main() -> RiseTask:
    return Top500Task(
        nome="Reativa Top",
        descricao="Torna todos os inativos ou que \
                           migraram e voltaram a aparecer na última leitura em vigiar.",
    )
