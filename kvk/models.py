from django.db import models
from datetime import date

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
    date = models.DateField(auto_now_add=True)

class AdicionalDeFarms(models.Model):
    kvk = models.ForeignKey(Kvk, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    t4_deaths = models.IntegerField(default=0)
    t5_deaths = models.IntegerField(default=0)