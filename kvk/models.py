from django.db import models
from datetime import date

from players.models import Player, PlayerStatus, Alliance

# Create your models here.
kvk_choices = (
    ('HA', 'Hino Heróico'),
    ('C8', 'Conflito dos 8'),
)


class Kvk(models.Model):
    inicio = models.DateField(default=date.today, unique=True)
    tipo = models.CharField(max_length=2, choices=kvk_choices, default='HA')
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f'KvK iniciado em {self.inicio}'


class Desempenho(models.Model):
    kvk = models.ForeignKey(Kvk, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    honra = models.IntegerField(default=0)
    primeiro_status = models.ForeignKey(
        PlayerStatus, related_name='kvkprimeirostatus', on_delete=models.CASCADE)
    ultimo_status = models.ForeignKey(
        PlayerStatus, related_name='kvkultimostatus', on_delete=models.CASCADE)
    data = models.DateField('Levantado em', default=date.today)
    zerado = models.BooleanField(default=False)

    def __str__(self):
        return f'Desempenho de {self.player.nick} no {self.kvk}'

    def kills(self):
        return self.ultimo_status.killpoints - self.primeiro_status.killpoints

    def deaths(self):
        return self.ultimo_status.deaths - self.primeiro_status.deaths
