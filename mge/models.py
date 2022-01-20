from django.db import models
from datetime import date, timedelta, datetime

from players.models import Player

# Create your models here.


class Mge(models.Model):
    criado_em = models.DateField("Criado em", default=date.today)

    class Meta:
        ordering = ["criado_em"]

    def semana(self):
        dia_da_semana = self.criado_em.weekday() + 1
        diferenca = timedelta(days=(7 - dia_da_semana))
        domingo = self.criado_em + diferenca
        return domingo

    def __str__(self):
        return f"MGE iniciado em {self.semana()}"


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

    inserido = models.DateTimeField("Inserido", auto_now_add=True)
