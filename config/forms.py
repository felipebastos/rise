from django import forms
from django.forms import inlineformset_factory

from config.models import Destaque, SiteConfig


class ConfigForm(forms.ModelForm):
    class Meta:
        model = SiteConfig
        fields = "__all__"
        widgets = {
            "prazo_inscricao_mge": forms.Select(
                attrs={"class": "form-select"}
            ),
            "encerra_ranking": forms.Select(attrs={"class": "form-select"}),
            "banner": forms.Textarea(attrs={"class": "form-control"}),
        }


DestaqueFormSet = inlineformset_factory(
    SiteConfig,
    Destaque,
    fields=("texto",),
    widgets={"texto": forms.TextInput(attrs={"class": "form-control"})},
    extra=1,
    can_delete_extra=False,
)
