from datetime import date, timedelta

from django.db import models
from django.utils import timezone

from players.models import Alliance, Player

# Create your models here.
resources = (
    ("COM", "Comida"),
    ("MAD", "Madeira"),
    ("PED", "Pedra"),
    ("OUR", "Ouro"),
)


class Semana(models.Model):
    segunda = models.DateField("Segunda", default=date.today)
    encerrada = models.BooleanField("Trabalhos concluídos", default=False)

    recurso = models.CharField(
        "Material", max_length=15, choices=resources, default="COM"
    )

    def inicio(self):
        dia_da_semana = self.segunda.weekday() + 1
        diferenca = timedelta(days=8 - dia_da_semana)
        segunda_seguinte = self.segunda + diferenca
        return segunda_seguinte

    def final(self):
        return self.inicio() + timedelta(days=6)

    def recurso_da_semana(self):
        for cod, val in resources:
            if cod == self.recurso:
                return val
        return None

    def __str__(self):
        return (
            f"Semana de {self.inicio()} a {self.final()} - {self.recurso_da_semana()}"
        )


class Donation(models.Model):
    data_da_doacao = models.DateField("Data da doação", default=date.today)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, default=None)
    donated = models.BooleanField("Doação realizada", default=False)

    semana = models.ForeignKey(Semana, on_delete=models.CASCADE, default=None)

    def getid(self):
        return str(self.id)

    def __str__(self):
        return f"Doação de {self.player.alliance.tag} {self.player.nick}"


class Credito(models.Model):
    ally = models.ForeignKey(Alliance, verbose_name="Aliança", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    quantidade = models.FloatField("Quantidade em milhões", blank=False)

    def __str__(self) -> str:
        return f"[{self.ally.tag}] tem {self.quantidade}"
