from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from datetime import date, datetime, timedelta

# Create your models here.
player_status = (
    ("PLAYER", "Player"),
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
    specialty = models.CharField(
        max_length=30, choices=player_spec, default="end"
    )
    status = models.CharField(
        max_length=100, default="ATIVO", choices=player_status
    )
    observacao = models.TextField(
        max_length=500, blank=True, null=True, default=""
    )
    alliance = models.ForeignKey(
        Alliance, on_delete=models.CASCADE, default=None, null=True
    )

    alterado_em = models.DateField("Alterado em", default=date.today)
    alterado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.nick}"

    class Meta:
        ordering = ["nick"]


class PlayerStatus(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    power = models.IntegerField(null=True)
    killpoints = models.IntegerField()
    deaths = models.IntegerField()

    def editavel(self):
        passou = datetime.now(timezone(-timedelta(hours=3))) - self.data
        return True if passou < timedelta(hours=1) else False

    def revisavel(self):
        passou = datetime.now(timezone(-timedelta(hours=3))) - self.data
        return False if passou < timedelta(days=2) else True

    def get_id(self):
        return str(self.id)

    def __str__(self):
        return f"{self.player.game_id} - {self.player.nick} - {self.data}"


class Advertencia(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    inicio = models.DateTimeField(auto_now_add=True)
    duracao = models.IntegerField(null=False, default=1)
    descricao = models.TextField(max_length=500)

    def final(self):
        return self.inicio + timedelta(days=self.duracao)

    def is_restrito(self):
        return True if timezone.now() < self.final() else False
