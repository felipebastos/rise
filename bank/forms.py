from django import forms

from bank.models import Credito


class CreditoForm(forms.ModelForm):
    class Meta:
        model = Credito
        fields = ["ally", "quantidade"]
        widgets = {
            "ally": forms.Select(attrs={"class": "form-select"}),
            "quantidade": forms.NumberInput(
                attrs={"class": "form-control", "value": "0"}
            ),
        }
