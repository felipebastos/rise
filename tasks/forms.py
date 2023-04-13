from django import forms
from django.conf import settings

from tasks.models import Task

SCRIPTS = (
    (filename, filename)
    for filename in settings.TASK_DIR
    if filename not in ["__pycache__", "script.py"]
)


class ConfiguraTask(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["uuid", "script"]
        widgets = {
            "uuid": forms.TextInput(
                attrs={"class": "form-control", "readonly": "true"}
            ),
            "script": forms.Select(attrs={"class": "form-select"}, choices=SCRIPTS),
        }
