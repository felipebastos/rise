from datetime import date, timedelta

from django.db import models
from django.utils import timezone

from players.models import Player

# Create your models here.
tipos_comandantes = (
    ("arc", "arquearia"),
    ("cav", "cavalaria"),
    ("inf", "infantaria"),
    ("lid", "liderança"),
    ("ndf", "não definido"),
)

COMMANDER_CHOICES = (
    ("0", "Não definido"),
    ("1", "Infantaria"),
    ("2", "Cavalaria"),
    ("3", "Arquearia"),
    ("4", "Liderança"),
    ("5", "Infantaria + Lançamento"),
    ("6", "Cavalaria + Lançamento"),
    ("7", "Arqueria + Lançamento"),
    ("8", "Liderança + Lançamento"),
)

COMMANDERS = [
    [
        "Constantino",
        "Pakal",
        "Leônidas",
        "Zenobia",
        "Flavius",
    ],
    ["Chandra", "Attila", "Bertrand", "Saladin", "Jadwiga", "Zika"],
    [
        "Tomirys",
        "Artemísia",
        "Amanitore",
        "Nabuco",
        "Henry",
    ],
    [
        "Wu Zetian",
        "Theodora",
        "Monteczuma",
        "Suleiman",
    ],
]


class Mge(models.Model):
    criado_em = models.DateField("Criado em", default=date.today)
    inicio_das_inscricoes = models.DateField("Início das inscrições", null=True)
    tipo = models.CharField(
        "Tipo", max_length=2, choices=COMMANDER_CHOICES, default="0"
    )
    tipo_mge = models.CharField(
        "Tipo de MGE", max_length=3, choices=tipos_comandantes, default="ndf"
    )

    temporada = models.IntegerField(default=0)
    livre = models.BooleanField(default=False)

    class Meta:
        ordering = ["criado_em"]

    def semana(self):
        domingo = None
        if not self.inicio_das_inscricoes:
            dia_da_semana = self.criado_em.weekday() + 1
            diferenca = timedelta(days=(7 - dia_da_semana))
            domingo = self.criado_em + diferenca
        else:
            dia_da_semana = self.inicio_das_inscricoes.weekday() + 1
            diferenca = timedelta(days=(7 - dia_da_semana))
            domingo = self.inicio_das_inscricoes + diferenca
        return domingo

    def __str__(self):
        if self.tipo != 0:
            return f"Temporada {self.temporada} - {COMMANDER_CHOICES[int(self.tipo)][1]} [{'LIVRE' if self.livre else 'CONTROLADO'}] iniciado em"
        return f"Temporada {self.temporada} - {tipos_comandantes[self.tipo_mge][1]} [{'LIVRE' if self.livre else 'CONTROLADO'}] iniciado em"


class Punido(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    mge = models.ForeignKey(Mge, on_delete=models.CASCADE)

    inserido = models.DateTimeField("Inserido", default=timezone.now)

    def __str__(self):
        return f"Punido no {self.mge}"


class Ranking(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    mge = models.ForeignKey(Mge, on_delete=models.CASCADE)

    inserido = models.DateTimeField("Inserido", default=timezone.now)


class Inscrito(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    mge = models.ForeignKey(Mge, on_delete=models.CASCADE)

    kills = models.BigIntegerField(default=0)
    deaths = models.IntegerField(default=0)

    general = models.TextField(default="")

    intuito = models.BooleanField(default=False)

    situacao = models.CharField(max_length=5, default="0000")
    gh = models.IntegerField(default=0)
    prioridade = models.BooleanField(default=False)

    inserido = models.DateTimeField("Inserido", default=timezone.now)

    def __str__(self) -> str:
        return f"{self.player} pediu {self.general} em {self.inserido}"


class Comandante(models.Model):
    nome = models.TextField()
    tipo = models.CharField(
        max_length=3, choices=tipos_comandantes, default="arc"
    )


class EventoDePoder(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    inserido = models.DateTimeField("Inserido", default=timezone.now)

    def __str__(self):
        return "Punido no evento de poder de"
