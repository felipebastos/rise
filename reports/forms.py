from django import forms

from players.models import PLAYER_STATUS, Alliance

FILTRA_PODER = (
    ("0", "0"),
    ("10000000", "10M"),
    ("20000000", "20M"),
    ("30000000", "30M"),
    ("40000000", "40M"),
    ("50000000", "50M"),
    ("60000000", "60M"),
    ("70000000", "70M"),
    ("80000000", "80M"),
    ("90000000", "90M"),
    ("100000000", "100M"),
    ("200000000", "200M"),
)

ORDER = (
    ("power", "poder"),
    ("killpoints", "killpoints"),
    ("deaths", "mortes"),
)


class FiltroForm(forms.Form):
    order = forms.ChoiceField(
        label="Ordenar por",
        choices=ORDER,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    poder_max = forms.ChoiceField(
        choices=FILTRA_PODER,
        label="Poder máximo",
        widget=forms.Select(attrs={"class": "form-select"}),
        required=True,
    )
    poder_min = forms.ChoiceField(
        choices=FILTRA_PODER,
        label="Poder mínimo",
        widget=forms.Select(attrs={"class": "form-select"}),
        required=True,
    )
    alianca = forms.ModelMultipleChoiceField(
        queryset=Alliance.objects.all().order_by("tag"),
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
    )

    status = forms.MultipleChoiceField(
        choices=PLAYER_STATUS,
        label="Status",
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
        required=False,
    )
