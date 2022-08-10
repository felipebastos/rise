from django.db import models
from datetime import date

from django.utils import timezone

from players.models import Player


# Create your models here.
kvk_choices = (
    ("HA", "Hino Heróico"),
    ("C8", "Conflito dos 8"),
)


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
        return f'Player {self.player} no KvK {self.kvk}'

class AdicionalDeFarms(models.Model):
    kvk = models.ForeignKey(Kvk, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    t4_deaths = models.IntegerField(default=0)
    t5_deaths = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'Adicional de {self.player} no KvK {self.kvk}'


class Etapas(models.Model):
    kvk = models.ForeignKey(Kvk, on_delete=models.CASCADE)
    date = models.DateTimeField()
    descricao = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'Etapa {self.descricao} do KvK {self.kvk}'
