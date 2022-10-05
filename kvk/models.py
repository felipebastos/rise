from datetime import date
from django.db import models

from django.utils import timezone

from players.models import Player


# Create your models here.
kvk_choices = (
    ("HA", "Hino Heróico"),
    ("C8", "Conflito dos 8"),
)

faixas = [
    (100000001, 5000000000, 3000000),
    (90000001, 100000000, 2200000),
    (80000001, 90000000, 1500000),
    (70000001, 80000000, 1100000),
    (60000001, 70000000, 700000),
    (50000001, 60000000, 600000),
    (40000001, 50000000, 500000),
    (0, 40000000, 500000),
]


class Kvk(models.Model):
    inicio = models.DateField(default=date.today, unique=True)
    final = models.DateField(null=True)
    tipo = models.CharField(max_length=2, choices=kvk_choices, default="HA")
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"KvK iniciado em {self.inicio}"


class Zerado(models.Model):
    kvk = models.ForeignKey(Kvk, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)

    def __str__(self) -> str:
        return f"Player {self.player} no KvK {self.kvk}"


class AdicionalDeFarms(models.Model):
    kvk = models.ForeignKey(Kvk, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    t4_deaths = models.IntegerField(default=0)
    t5_deaths = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"Adicional de {self.player} no KvK {self.kvk}"


class PontosDeMGE(models.Model):
    kvk = models.ForeignKey(Kvk, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    pontos = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"Pontos de MGE de {self.player} no KvK {self.kvk}"


class Etapas(models.Model):
    kvk = models.ForeignKey(Kvk, on_delete=models.CASCADE)
    date = models.DateTimeField()
    descricao = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"Etapa {self.descricao} do KvK {self.kvk}"


FUNCAO_CHOICES = (("ral", "Rali"), ("gua", "Guarnição"))


class Cargo(models.Model):
    kvk = models.ForeignKey(Kvk, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    funcao = models.CharField(
        max_length=3, choices=FUNCAO_CHOICES, default="ral"
    )
