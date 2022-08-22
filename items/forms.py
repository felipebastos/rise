from django import forms

from items.models import Item


class PedidoForm(forms.Form):
    player = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Seu ID",
            }
        )
    )
    item = forms.ModelChoiceField(
        queryset=Item.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"}),
        required=True,
    )
    quantidade = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        required=True,
        initial=1,
        min_value=1,
    )
