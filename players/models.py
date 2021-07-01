from django.db import models
from datetime import date

# Create your models here.
player_status = (
    ('ATIVO', 'Ativo'),
    ('INATIVO', 'Inativo'),
    ('MIGROU', 'Migrou'),
    ('VIGIAR', 'Vigiar'),
    ('BANIDO', 'BANIDO')
)
player_rank = (
    ('R5', 'R5'),
    ('R4', 'R4'),
    ('R3', 'R3'),
    ('R2', 'R2'),
    ('R1', 'R1')
)


class Alliance(models.Model):
    nome = models.CharField(max_length=100)
    tag = models.CharField(max_length=4)


class Player(models.Model):
    game_id = models.CharField(max_length=8)
    nick = models.CharField(max_length=100)
    rank = models.CharField(max_length=2, choices=player_rank, default='R1')
    status = models.CharField(
        max_length=100, default='ATIVO', choices=player_status)
    alliance = models.ForeignKey(Alliance, on_delete=models.CASCADE, default=None)


class PlayerStatus(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    data = models.DateField(default=date.today)
    power = models.IntegerField()
    killpoints = models.IntegerField()
    deaths = models.IntegerField()
