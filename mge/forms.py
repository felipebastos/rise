from django import forms

COMMANDER_CHOICES = (
    ("0", "Não definido"),
    ("1", "Infantaria"),
    ("2", "Cavalaria"),
    ("3", "Arquearia"),
    ("4", "Liderança"),
    ("5", "Infantaria + Lançamento"),
    ("6", "Cavalaria + Lançamento"),
    ("7", "Arqueria + Lançamento"),
    ("8", "Liderança + Lançamento"),
)

COMMANDERS = [
    [
        "Constantino",
        "Pakal",
        "Leônidas",
        "Zenobia",
        "Flavius",
    ],
    [
        "Chandra",
        "Attila",
        "Bertrand",
        "Saladin",
        "Jadwiga",
    ],
    [
        "Tomirys",
        "Artemísia",
        "Amanitore",
        "Nabuco",
        "Henry",
    ],
    [
        "Wu Zetian",
        "Theodora",
        "Monteczuma",
        "Suleiman",
    ],
]


class CriaMGE(forms.Form):
    commanders = forms.ChoiceField(
        label="Escolha o tipo do MGE",
        choices=COMMANDER_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
        initial="0",
    )
    controle = forms.ChoiceField(
        label="O MGE é livre?",
        choices=(("0", 'Sim'), ("1", 'Não')),
        widget=forms.Select(attrs={"class": "form-select"}),
        initial="1",
    )
