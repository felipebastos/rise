from django.db import models
from datetime import date, timedelta

from players.models import Player

# Create your models here.
class Semana(models.Model):
    segunda = models.DateField('Segunda', default=date.today)
    encerrada = models.BooleanField('Trabalhos concluídos', default=False)

    def inicio(self):
        dia_da_semana = self.segunda.weekday()+1
        diferenca = timedelta(days=(8-dia_da_semana))
        segunda_seguinte = self.segunda + diferenca
        return segunda_seguinte

    def final(self):
        return self.inicio() + timedelta(days=6)


    def __str__(self):
        return f'Semana de {self.inicio()} a {self.final()}'

class Donation(models.Model):
    data_da_doacao = models.DateField('Data da doação', default=date.today)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, default=None)
    donated = models.BooleanField('Doação realizada', default=False)

    semana = models.ForeignKey(Semana, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f'Doação de {self.player.alliance.tag} {self.player.nick}'
