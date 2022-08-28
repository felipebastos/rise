from django import forms

from osiris.models import TIMES, Time, Marcha
from players.models import Player


class ArcaForm(forms.ModelForm):
    class Meta:
        model = Time
        fields = ["ally"]
        widgets = {
            "ally": forms.Select(attrs={"class": "form-select"}),
        }


class TimeForm(forms.Form):
    player = forms.ModelChoiceField(
        queryset=Player.objects.exclude(
            status__in=["BANIDO", "FARM", "MIGROU", "INATIVO"]
        ),
        label="Player",
        widget=forms.Select(attrs={"class": "form-select"}),
        required=True,
    )
    lado = forms.ChoiceField(
        choices=TIMES,
        label="Lado",
        widget=forms.Select(attrs={"class": "form-select"}),
        required=True,
    )


class MarchaForm(forms.ModelForm):
    class Meta:
        model = Marcha
        fields = ["tipo", "tarefa", "estrutura", "tarefa_especial"]
        widgets = {
            "tipo": forms.Select(attrs={"class": "form-select"}),
            "tarefa": forms.Select(attrs={"class": "form-select"}),
            "estrutura": forms.Select(attrs={"class": "form-select"}),
            "tarefa_especial": forms.Select(attrs={"class": "form-select"}),
        }
