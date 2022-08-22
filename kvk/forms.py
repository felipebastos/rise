from django import forms

from kvk.models import Kvk

class EtapaForm(forms.Form):
    kvk = forms.ModelChoiceField(queryset=Kvk.objects.all(), label="KvK", widget=forms.Select(attrs={'class': 'form-select'}), required=True)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label='Data da etapa', required=True)
    descricao = forms.CharField(label="Qual etapa?", widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)


class UploadEtapasFileForm(forms.Form):
    file = forms.FileField(label='Planilha', widget=forms.FileInput(attrs={'class': 'form-control'}), required=True)
