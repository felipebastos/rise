from django import forms


class UploadFileForm(forms.Form):
    """
    Formulário para upload de arquivo.

    Fields:
        - file: campo para selecionar o arquivo a ser enviado.
    """

    file = forms.FileField()
    dia = forms.DateField(
        label="Dia",
        required=True,
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )


class AddFarmForm(forms.Form):
    """
    Formulário para adicionar uma fazenda.

    Fields:
        - farm: campo para inserir o nome da fazenda.
    """

    farm = forms.CharField(
        label="Farm a adicionar",
        max_length=9,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "pattern": "^[0-9]*$"}),
    )
