from django import forms

from kvk.models import Cargo, Kvk, KvKStatus


class EtapaForm(forms.Form):
    kvk = forms.ModelChoiceField(
        queryset=Kvk.objects.all(),
        label="KvK",
        widget=forms.Select(attrs={"class": "form-select"}),
        required=True,
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        label="Data da etapa",
        required=True,
    )
    descricao = forms.CharField(
        label="Qual etapa?",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True,
    )


class UploadEtapasFileForm(forms.Form):
    file = forms.FileField(
        label="Planilha",
        widget=forms.FileInput(attrs={"class": "form-control"}),
        required=True,
    )


class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = "__all__"
        widgets = {
            "kvk": forms.Select(attrs={"class": "form-select"}),
            "player": forms.Select(attrs={"class": "form-select"}),
            "funcao": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {
            "funcao": "Função",
        }


class KvkConfigForm(forms.ModelForm):
    class Meta:
        model = Kvk
        fields = ["inicio", "tipo", "primeira_luta", "final"]
        widgets = {
            "inicio": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={"type": "date", "class": "form-control"},
            ),
            "final": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={"type": "date", "class": "form-control"},
            ),
            "tipo": forms.Select(attrs={"class": "form-select"}),
            "primeira_luta": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={"type": "date", "class": "form-control"},
            ),
        }
        labels = {
            "primeira_luta": "Primeira luta",
        }


class KvKStatusForm(forms.ModelForm):
    class Meta:
        model = KvKStatus
        fields = ["deatht4", "deatht5", "honra", "marauders"]

        widgets = {
            "deatht4": forms.NumberInput(attrs={"class": "form-control"}),
            "deatht5": forms.NumberInput(attrs={"class": "form-control"}),
            "honra": forms.NumberInput(attrs={"class": "form-control"}),
            "marauders": forms.NumberInput(attrs={"class": "form-control"}),
        }
