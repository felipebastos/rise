from django import forms

from config.models import SiteConfig


class ConfigForm(forms.ModelForm):
    class Meta:
        model = SiteConfig
        fields = "__all__"
        widgets = {
            "prazo_inscricao_mge": forms.Select(attrs={"class": "form-select"}),
            "encerra_ranking": forms.Select(attrs={"class": "form-select"}),
        }
