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

CARGO = (
    ("open", "Openfield"),
    ("rali", "Rali"),
    ("guar", "Guarnição"),
)


class Alliance(models.Model):
    """
    Armazena os dados básicos de uma aliança.
    Uma aliança é formada por um grupo de cerca de 150 jogadores.

    Fields:
        - nome (str): Nome da aliança.
        - tag (str): Tag da aliança.
    """

    nome = models.CharField(max_length=100)
    tag = models.CharField(max_length=4)

    def __str__(self):
        return f"{self.tag} - {self.nome}"


class Player(models.Model):
    """
    Armazena os dados de um jogador.

    Fields:
        - game_id (str): ID do jogo do jogador.
        - nick (str): Apelido do jogador.
        - rank (str): Classificação do jogador.
        - specialty (str): Especialidade do jogador.
        - status (str): Status do jogador.
        - observacao (str): Observação sobre o jogador.
        - alliance (Alliance): Aliança do jogador.
        - func (str): Função do jogador.
        - farms (QuerySet): Jogadores que são fazendas para este jogador.
        - alterado_em (date): Data de alteração do jogador.
        - alterado_por (User): Usuário que realizou a alteração do jogador.

    Meta:
        ordering (list): Lista de campos para ordenação dos jogadores.
    """

    game_id = models.CharField(max_length=12, unique=True)
    nick = models.CharField(max_length=100)
    rank = models.CharField(max_length=2, choices=player_rank, default="R1")
    specialty = models.CharField(max_length=30, choices=player_spec, default="end")
    status = models.CharField(max_length=100, default="PLAYER", choices=PLAYER_STATUS)
    observacao = models.TextField(max_length=500, blank=True, null=True, default="")
    alliance = models.ForeignKey(
        Alliance, on_delete=models.CASCADE, default=None, null=True
    )

    func = models.CharField(max_length=4, choices=CARGO, default="open")

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
    """
    Armazena o status de um jogador em um determinado momento.

    Fields:
        - player (Player): Jogador associado ao status.
        - data (datetime): Data e hora do status.
        - power (int): Poder do jogador.
        - killpoints (int): Pontos de morte do jogador.
        - deaths (int): Número de mortes do jogador.
    """

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    data = models.DateTimeField(default=tz.now)
    power = models.IntegerField(null=True)
    killpoints = models.BigIntegerField()
    deaths = models.IntegerField()

    killst4 = models.BigIntegerField(default=0)
    killst5 = models.BigIntegerField(default=0)

    def editavel(self):
        """
        Verifica se o objeto é editável com base
        na diferença entre a data atual e a data do objeto.

        Returns:
            bool: True se o objeto for editável, False caso contrário.
        """
        passou = datetime.now(timezone(-timedelta(hours=3))) - self.data
        return passou < timedelta(hours=1)

    def revisavel(self):
        """
        Verifica se o objeto é revisável.

        Retorna True se o objeto não foi revisado nos últimos 2 dias,
        caso contrário, retorna False.

        Returns:
            bool: True se o objeto for revisável, False caso contrário.
        """
        passou = datetime.now(timezone(-timedelta(hours=3))) - self.data
        return not passou < timedelta(days=2)

    def get_id(self):
        return str(self.id)

    def __str__(self):
        return f"{self.player.game_id} - {self.player.nick} - {self.data}"


class Advertencia(models.Model):
    """
    Armazena as advertências de um jogador.

    Fields:
        - player (Player): Jogador associado à advertência.
        - inicio (datetime): Data e hora de início da advertência.
        - duracao (int): Duração da advertência em dias.
        - descricao (str): Descrição da advertência.
    """

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    inicio = models.DateTimeField(default=tz.now)
    duracao = models.IntegerField(null=False, default=1)
    descricao = models.TextField(max_length=500)

    def final(self):
        """
        Retorna a data final da advertência somando a data de início com a duração.

        Returns:
            datetime.datetime: A data final calculada.
        """
        return self.inicio + timedelta(days=self.duracao)

    def is_restrito(self):
        """
        Verifica se o objeto está restrito com base na data atual.

        Returns:
            bool: True se o objeto estiver restrito, False caso contrário.
        """
        return tz.now() < self.final()
