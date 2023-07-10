from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()


class AddFarmForm(forms.Form):
    farm = forms.CharField(
        label="Farm a adicionar",
        max_length=9,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "pattern": "^[0-9]*$"}),
    )
