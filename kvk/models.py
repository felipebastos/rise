from django.db import models
from datetime import date

# Create your models here.
kvk_choices = (
    ('HA', 'Hino Heróico'),
    ('C8', 'Conflito dos 8'),
)


class Kvk(models.Model):
    inicio = models.DateField(default=date.today, unique=True)
    tipo = models.CharField(max_length=2, choices=kvk_choices, default='HA')
