from django import forms
from django.forms import inlineformset_factory

from equipments.models import Buff, Equipamento


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = "__all__"
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "miniatura": forms.FileInput(attrs={"class": "form-control"}),
            "slot": forms.Select(attrs={"class": "form-select"}),
        }


BuffFormSet = inlineformset_factory(
    Equipamento,
    Buff,
    fields=("spec", "status", "valor", "ativacao"),
    widgets={
        "spec": forms.Select(attrs={"class": "form-select"}),
        "status": forms.Select(attrs={"class": "form-select"}),
        "valor": forms.NumberInput(
            attrs={"class": "form-control", "value": "0"}
        ),
        "ativacao": forms.NumberInput(
            attrs={
                "class": "form-range",
                "type": "range",
                "value": "1.0",
                "min": "0.0",
                "max": "1.0",
                "step": "0.05",
                "onchange": "update()",
            }
        ),
    },
    extra=4,
    can_delete_extra=True,
)


class EquipForm(forms.Form):
    capacete = forms.ModelChoiceField(
        queryset=Equipamento.objects.filter(slot="cap"),
        widget=forms.Select(attrs={"class": "form-select"}),
        required=False,
    )
    peitoral = forms.ModelChoiceField(
        queryset=Equipamento.objects.filter(slot="pei"),
        widget=forms.Select(attrs={"class": "form-select"}),
        required=False,
    )
    armamento = forms.ModelChoiceField(
        queryset=Equipamento.objects.filter(slot="arm"),
        widget=forms.Select(attrs={"class": "form-select"}),
        required=False,
    )
    luva = forms.ModelChoiceField(
        queryset=Equipamento.objects.filter(slot="luv"),
        widget=forms.Select(attrs={"class": "form-select"}),
        required=False,
    )
    calca = forms.ModelChoiceField(
        label="Calça",
        queryset=Equipamento.objects.filter(slot="cal"),
        widget=forms.Select(attrs={"class": "form-select"}),
        required=False,
    )
    botas = forms.ModelChoiceField(
        queryset=Equipamento.objects.filter(slot="bot"),
        widget=forms.Select(attrs={"class": "form-select"}),
        required=False,
    )
    ace = forms.ModelChoiceField(
        label="Acessório da esquerda",
        queryset=Equipamento.objects.filter(slot="ace"),
        widget=forms.Select(attrs={"class": "form-select"}),
        required=False,
    )
    acd = forms.ModelChoiceField(
        label="Acessório da direita",
        queryset=Equipamento.objects.filter(slot="acd"),
        widget=forms.Select(attrs={"class": "form-select"}),
        required=False,
    )
