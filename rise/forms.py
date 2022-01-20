from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "nome de usuário"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "nome de usuário"}
        )
    )
    captcha = CaptchaField()


class SearchPlayerForm(forms.Form):
    id = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "nome de usuário",
                "pattern": "^[0-9]*$",
                "placeholder": "ID do jogador",
                "min": "0",
            }
        )
    )
