from django.db import models

# Create your models here.
PRAZO_MGE_INSC = (
    (5, "Terça-feira"),
    (4, "Quarta-feira"),
    (3, "Quinta-feira"),
    (2, "Sexta-feira"),
    (1, "Sábado"),
    (0, "Domingo"),
)

PRAZO_RANKING = (
    (0, "Domingo"),
    (1, "Segunda-feira"),
    (2, "Terça-feira"),
    (3, "Quarta-feira"),
    (4, "Quinta-feira"),
    (6, "Sexta-feira"),
    (7, "Sábado"),
)


class SiteConfig(models.Model):
    prazo_inscricao_mge = models.IntegerField(
        "Prazo para inscrição em MGE", choices=PRAZO_MGE_INSC, default=3
    )
    encerra_ranking = models.IntegerField(
        "Prazo para travar o ranking do MGE", choices=PRAZO_RANKING, default=4
    )
    banner = models.TextField(default="")


class Destaque(models.Model):
    config = models.ForeignKey(
        SiteConfig, related_name="destaques", on_delete=models.CASCADE
    )

    texto = models.CharField("Texto do destaque", max_length=144)
