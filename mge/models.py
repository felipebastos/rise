from django.db import models
from datetime import date, timedelta, datetime
from mge.forms import COMMANDER_CHOICES

from players.models import Player

# Create your models here.
tipos_comandantes = (
    ("arc", "arquearia"),
    ("cav", "cavalaria"),
    ("inf", "infantaria"),
    ("lid", "liderança"),
    ("ndf", "não definido"),
)

class Mge(models.Model):
    criado_em = models.DateField("Criado em", default=date.today)
    tipo = models.CharField(
        "Tipo", max_length=2, choices=COMMANDER_CHOICES, default="0"
    )
    tipo_mge = models.CharField("Tipo de MGE", max_length=3, choices=tipos_comandantes, default="ndf")

    class Meta:
        ordering = ["criado_em"]

    def semana(self):
        dia_da_semana = self.criado_em.weekday() + 1
        diferenca = timedelta(days=(7 - dia_da_semana))
        domingo = self.criado_em + diferenca
        return domingo

    def __str__(self):
        if self.tipo != 0:
            return f"MGE de {COMMANDER_CHOICES[int(self.tipo)][1]} iniciado em"
        else:
            return f"MGE de {tipos_comandantes[self.tipo_mge][1]} iniciado em"


class Punido(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    mge = models.ForeignKey(Mge, on_delete=models.CASCADE)

    inserido = models.DateTimeField("Inserido", auto_now_add=True)

    def __str__(self):
        return f"Punido no {self.mge}"


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

    intuito = models.BooleanField(default=False)

    inserido = models.DateTimeField("Inserido", auto_now_add=True)


class Comandante(models.Model):
    nome = models.TextField()
    tipo = models.CharField(max_length=3, choices=tipos_comandantes, default="arc")


class EventoDePoder(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    
    inserido = models.DateTimeField("Inserido", auto_now_add=True)

    def __str__(self):
        return f"Punido no evento de poder de"