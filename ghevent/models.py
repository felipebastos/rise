from django.db import models
from django.utils import timezone

from players.models import Player

EVENTO_TIPO = (
    ("pow", "poder"),
    ("acc", "aceleração"),
)


# Create your models here.
class EventoGH(models.Model):
    criado_em = models.DateField("Criado em", auto_now_add=True)
    data_evento = models.DateField("Data do evento")

    tipo = models.CharField(max_length=3, choices=EVENTO_TIPO, default="pow")

    anotacao = models.CharField(max_length=200, null=True)


class InscritoGH(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    evento = models.ForeignKey(EventoGH, on_delete=models.CASCADE)

    kills = models.BigIntegerField(default=0)
    deaths = models.IntegerField(default=0)

    inserido = models.DateTimeField("Inserido", default=timezone.now)
