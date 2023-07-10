from datetime import date, datetime, timedelta, timezone

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone as tz

# Create your models here.
PLAYER_STATUS = (
    ("PLAYER", "Player"),
    ("SECUNDARIA", "Secundária"),
    ("FARM", "Farm"),
    ("INATIVO", "Inativo"),
    ("MIGROU", "Migrou"),
    ("VIGIAR", "Vigiar"),
    ("BANIDO", "BANIDO"),
)
player_rank = (
    ("R5", "R5"),
    ("R4", "R4"),
    ("R3", "R3"),
    ("R2", "R2"),
    ("R1", "R1"),
    ("SA", "SA"),
)

player_spec = (
    ("arq", "Arquearia"),
    ("cav", "Cavalaria"),
    ("lid", "Liderança"),
    ("inf", "Infantaria"),
    ("end", "Especialidade não definida"),
)


class Alliance(models.Model):
    nome = models.CharField(max_length=100)
    tag = models.CharField(max_length=4)

    def __str__(self):
        return f"{self.tag} - {self.nome}"


class Player(models.Model):
    game_id = models.CharField(max_length=9, unique=True)
    nick = models.CharField(max_length=100)
    rank = models.CharField(max_length=2, choices=player_rank, default="R1")
    specialty = models.CharField(max_length=30, choices=player_spec, default="end")
    status = models.CharField(max_length=100, default="PLAYER", choices=PLAYER_STATUS)
    observacao = models.TextField(max_length=500, blank=True, null=True, default="")
    alliance = models.ForeignKey(
        Alliance, on_delete=models.CASCADE, default=None, null=True
    )

    farms = models.ManyToManyField("Player", related_name="principal")

    alterado_em = models.DateField("Alterado em", default=date.today)
    alterado_por = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return f"{self.nick}"

    class Meta:
        ordering = ["nick"]


class PlayerStatus(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    data = models.DateTimeField(default=tz.now)
    power = models.IntegerField(null=True)
    killpoints = models.BigIntegerField()
    deaths = models.IntegerField()

    def editavel(self):
        passou = datetime.now(timezone(-timedelta(hours=3))) - self.data
        return passou < timedelta(hours=1)

    def revisavel(self):
        passou = datetime.now(timezone(-timedelta(hours=3))) - self.data
        return not passou < timedelta(days=2)

    def get_id(self):
        return str(self.id)

    def __str__(self):
        return f"{self.player.game_id} - {self.player.nick} - {self.data}"


class Advertencia(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    inicio = models.DateTimeField(default=tz.now)
    duracao = models.IntegerField(null=False, default=1)
    descricao = models.TextField(max_length=500)

    def final(self):
        return self.inicio + timedelta(days=self.duracao)

    def is_restrito(self):
        return tz.now() < self.final()
