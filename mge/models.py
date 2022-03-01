from django.db import models
from datetime import date, timedelta, datetime
from mge.forms import COMMANDER_CHOICES

from players.models import Player

# Create your models here.


class Mge(models.Model):
    criado_em = models.DateField("Criado em", default=date.today)
    tipo = models.CharField(
        "Tipo", max_length=2, choices=COMMANDER_CHOICES, default="0"
    )

    class Meta:
        ordering = ["criado_em"]

    def semana(self):
        dia_da_semana = self.criado_em.weekday() + 1
        diferenca = timedelta(days=(7 - dia_da_semana))
        domingo = self.criado_em + diferenca
        return domingo

    def __str__(self):
        return f"MGE de {COMMANDER_CHOICES[int(self.tipo)][1]} iniciado em"


class Punido(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    mge = models.ForeignKey(Mge, on_delete=models.CASCADE)

    inserido = models.DateTimeField("Inserido", auto_now_add=True)


class Ranking(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    mge = models.ForeignKey(Mge, on_delete=models.CASCADE)

    inserido = models.DateTimeField("Inserido", auto_now_add=True)


class Inscrito(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    mge = models.ForeignKey(Mge, on_delete=models.CASCADE)

    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)

    general = models.TextField(default="")

    inserido = models.DateTimeField("Inserido", auto_now_add=True)
