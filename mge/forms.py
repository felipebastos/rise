from django import forms

from mge.models import COMMANDER_CHOICES, Mge


class CriaMGE(forms.Form):
    commanders = forms.ChoiceField(
        label="Escolha o tipo do MGE",
        choices=COMMANDER_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
        initial="0",
    )
    controle = forms.ChoiceField(
        label="O MGE é livre?",
        choices=(("0", "Sim"), ("1", "Não")),
        widget=forms.Select(attrs={"class": "form-select"}),
        initial="1",
    )


class NovoCriaMGEForm(forms.ModelForm):
    class Meta:
        model = Mge
        fields = ["tipo", "inicio_das_inscricoes", "livre"]
        labels = {
            "livre": "O MGE é livre?",
        }
        widgets = {
            "tipo": forms.Select(attrs={"class": "form-select"}),
            "inicio_das_inscricoes": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                    "required": "true",
                },
            ),
            "livre": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
