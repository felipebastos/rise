from django.db import models

from players.models import Alliance, Player

# Create your models here.
TIPO_MARCHA = (
    ("inf", "Infantaria"),
    ("arq", "Arquearia"),
    ("cav", "Cavalaria"),
    ("mis", "Mista"),
    ("mqt", "Melhor que tiver"),
)

TAREFA = (
    ("open", "Open field"),
    ("guar", "Líder de Guarnição"),
    ("guae", "Encher Guarnição"),
    ("rall", "Líder de Rally"),
    ("rale", "Encher Rally"),
    ("swad", "Swarm defensivo"),
    ("swao", "Swarm ofensivo"),
)

ESTRUTURA = (
    ("obda", "Obelisco defensivo A"),
    ("obdb", "Obelisco defensivo B"),
    ("oboa", "Obelisco ofensivo A"),
    ("obob", "Obelisco ofensivo B"),
    ("sagd", "Santuário da Guerra defensivo"),
    ("sago", "Santuário da Guerra ofensivo"),
    ("alcd", "Altar do Céu defensivo"),
    ("alco", "Altar do Céu ofensivo"),
    ("aldd", "Altar do Deserto defensivo"),
    ("aldo", "Altar do Deserto ofensivo"),
    ("savd", "Santuário da Vida defensivo"),
    ("savo", "Santuário da Vida ofensivo"),
    ("poad", "Postos Avançados defensivos"),
    ("poao", "Postos Avançados ofensivos"),
    ("nenh", "Nenhuma estrutura"),
)

TAREFA_ESPECIAL = (
    ("rald", "Rally no obelisco defensivo"),
    ("ralo", "Rally no obelisco ofensivo"),
    ("arca", "Carregar arca"),
    ("meio", "Ir para o meio"),
    ("nenh", "Nenhuma"),
)

TIMES = (
    ("a", "Time A"),
    ("b", "Time B"),
)


class Marcha(models.Model):
    tipo = models.CharField(max_length=4, choices=TIPO_MARCHA, default="mqt")
    tarefa = models.CharField(max_length=4, choices=TAREFA, default="open")
    estrutura = models.CharField(
        max_length=4, choices=ESTRUTURA, default="nenh"
    )
    tarefa_especial = models.CharField(
        max_length=4, choices=TAREFA_ESPECIAL, default="nenh"
    )


class Funcao(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    marchas = models.ManyToManyField(Marcha)

    lado = models.CharField(
        max_length=2,
        choices=TIMES,
    )


class Time(models.Model):
    ally = models.ForeignKey(
        Alliance, verbose_name="Aliança", on_delete=models.CASCADE
    )

    funcoes = models.ManyToManyField(Funcao)
