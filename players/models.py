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
    ('R1', 'R1'),
    ('SA', 'SA')
)


class Alliance(models.Model):
    nome = models.CharField(max_length=100)
    tag = models.CharField(max_length=4)

    def __str__(self):
        return f'{self.tag} - {self.nome}'


class Player(models.Model):
    game_id = models.CharField(max_length=8)
    nick = models.CharField(max_length=100)
    rank = models.CharField(max_length=2, choices=player_rank, default='R1')
    status = models.CharField(
        max_length=100, default='ATIVO', choices=player_status)
    observacao = models.CharField(max_length=500, blank=True, null=True)
    alliance = models.ForeignKey(Alliance, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return f'{self.nick}'

    class Meta:
        ordering = ['nick']


class PlayerStatus(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    data = models.DateField(default=date.today)
    power = models.IntegerField(null=True)
    killpoints = models.IntegerField()
    deaths = models.IntegerField()

    def __str__(self):
        return f'{self.player.game_id} - {self.player.nick} - {self.data}'
