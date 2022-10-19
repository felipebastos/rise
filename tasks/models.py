from importlib import import_module

from uuid import uuid4

from django.db import models
from django.utils import timezone


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

    def executar(self) -> str:
        modulo = import_module(
            f"tasks.scripts.{self.script.split('.', maxsplit=1)[0]}"
        )
        resp = modulo.main()
        self.executou()

        return resp
