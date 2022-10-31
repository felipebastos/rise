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
        queryset=Equipamento.objects.filter(slot="cap").order_by("nome"),
        widget=forms.Select(attrs={"class": "form-select"}),
        required=False,
    )
    cap_spec = forms.BooleanField(
        label="Spec",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        required=False,
    )
    cap_icon = forms.BooleanField(
        label="Icônico",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        required=False,
    )
    peitoral = forms.ModelChoiceField(
        queryset=Equipamento.objects.filter(slot="pei").order_by("nome"),
        widget=forms.Select(attrs={"class": "form-select"}),
        required=False,
    )
    pei_spec = forms.BooleanField(
        label="Spec",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        required=False,
    )
    pei_icon = forms.BooleanField(
        label="Icônico",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        required=False,
    )
    armamento = forms.ModelChoiceField(
        queryset=Equipamento.objects.filter(slot="arm").order_by("nome"),
        widget=forms.Select(attrs={"class": "form-select"}),
        required=False,
    )
    arm_spec = forms.BooleanField(
        label="Spec",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        required=False,
    )
    arm_icon = forms.BooleanField(
        label="Icônico",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        required=False,
    )
    luva = forms.ModelChoiceField(
        queryset=Equipamento.objects.filter(slot="luv").order_by("nome"),
        widget=forms.Select(attrs={"class": "form-select"}),
        required=False,
    )
    luv_spec = forms.BooleanField(
        label="Spec",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        required=False,
    )
    luv_icon = forms.BooleanField(
        label="Icônico",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        required=False,
    )
    calca = forms.ModelChoiceField(
        label="Calça",
        queryset=Equipamento.objects.filter(slot="cal").order_by("nome"),
        widget=forms.Select(attrs={"class": "form-select"}),
        required=False,
    )
    cal_spec = forms.BooleanField(
        label="Spec",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        required=False,
    )
    cal_icon = forms.BooleanField(
        label="Icônico",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        required=False,
    )
    botas = forms.ModelChoiceField(
        queryset=Equipamento.objects.filter(slot="bot").order_by("nome"),
        widget=forms.Select(attrs={"class": "form-select"}),
        required=False,
    )
    bot_spec = forms.BooleanField(
        label="Spec",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        required=False,
    )
    bot_icon = forms.BooleanField(
        label="Icônico",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        required=False,
    )
    ace = forms.ModelChoiceField(
        label="Acessório da esquerda",
        queryset=Equipamento.objects.filter(slot="ace").order_by("nome"),
        widget=forms.Select(attrs={"class": "form-select"}),
        required=False,
    )
    ace_spec = forms.BooleanField(
        label="Spec",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        required=False,
    )
    ace_icon = forms.BooleanField(
        label="Icônico",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        required=False,
    )
    acd = forms.ModelChoiceField(
        label="Acessório da direita",
        queryset=Equipamento.objects.filter(slot="acd").order_by("nome"),
        widget=forms.Select(attrs={"class": "form-select"}),
        required=False,
    )
    acd_spec = forms.BooleanField(
        label="Spec",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        required=False,
    )
    acd_icon = forms.BooleanField(
        label="Icônico",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        required=False,
    )
