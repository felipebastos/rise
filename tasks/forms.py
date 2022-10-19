from django.conf import settings
from django import forms

from tasks.models import Task

SCRIPTS = (
    (filename, filename)
    for filename in settings.TASK_DIR
    if filename != "__pycache__"
)


class ConfiguraTask(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["uuid", "nome_da_task", "descricao", "script"]
        widgets = {
            "uuid": forms.TextInput(
                attrs={"class": "form-control", "readonly": "true"}
            ),
            "nome_da_task": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.TextInput(attrs={"class": "form-control"}),
            "script": forms.Select(
                attrs={"class": "form-select"}, choices=SCRIPTS
            ),
        }
