from django.db import models
from django.utils import timezone
from players.models import Player

# Create your models here.
class Item(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.nome


class Pedido(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantidade = models.IntegerField(blank=False)
    pedido_em = models.DateTimeField(default=timezone.now)
    avaliado = models.BooleanField(default=False)
    aprovado = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.player.nick} pediu {self.quantidade} {self.item}(s)"
