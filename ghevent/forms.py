from django import forms

from ghevent.models import EventoGH, InscritoGH


class EventoGHForm(forms.ModelForm):
    class Meta:
        model = EventoGH
        fields = ["data_evento", "tipo", "anotacao"]
        labels = {
            "data_evento": "Quando ocorre o evento?",
            "anotacao": "Qual a razão do ranking?",
        }
        widgets = {
            "data_evento": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                    "required": "true",
                },
            ),
            "tipo": forms.Select(attrs={"class": "form-select"}),
            "anotacao": forms.TextInput(attrs={"class": "form-control"}),
        }


class InscritoGHForm(forms.Form):
    busca = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "ID do jogador",
            }
        )
    )
