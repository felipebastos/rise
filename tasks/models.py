from importlib import import_module
from typing import Type

from uuid import uuid4
from django import forms

from django.db import models
from django.utils import timezone

from tasks.scripts.script import RiseTask, RiseTaskResponse


# Create your models here.
class Task(models.Model):
    uuid = models.UUIDField("ID único", default=uuid4, unique=True)
    nome_da_task = models.CharField(
        "Nome da task", max_length=40, default="Não nomeada"
    )
    ultima_execucao = models.DateTimeField("Última execução", null=True)
    descricao = models.CharField(
        "Descrição", max_length=500, default="Não fornecida"
    )
    script = models.CharField("Script", max_length=100, default="")

    def executou(self):
        self.ultima_execucao = timezone.now()
        self.save()

    def executar(self, from_form: forms.Form = None) -> RiseTaskResponse:
        modulo = import_module(
            f"tasks.scripts.{self.script.split('.', maxsplit=1)[0]}"
        )
        script: RiseTask = modulo.main()
        resp: RiseTaskResponse = script.run(from_form)
        self.executou()

        return resp

    def form(self) -> forms.Form:
        modulo = import_module(
            f"tasks.scripts.{self.script.split('.', maxsplit=1)[0]}"
        )
        script: RiseTask = modulo.main()
        form_instance = None
        if script.form_class() is not None:
            form_instance = script.form_class()()
        return form_instance

    def form_class(self) -> Type[forms.Form]:
        modulo = import_module(
            f"tasks.scripts.{self.script.split('.', maxsplit=1)[0]}"
        )
        script: RiseTask = modulo.main()
        return script.form_class()
