from django.db import models
from datetime import date

from players.models import Player

# Create your models here.
class Semana(models.Model):
    segunda = models.DateField('Segunda', default=date.today)
    encerrada = models.BooleanField('Trabalhos concluídos', default=False)

    def __str__(self):
        return f'Semana iniciada em {self.segunda}'

class Donation(models.Model):
    data_da_doacao = models.DateField('Data da doação', default=date.today)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, default=None)
    donated = models.BooleanField('Doação realizada', default=False)

    semana = models.ForeignKey(Semana, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f'Doação de {self.player.alliance.tag} {self.player.nick}'
