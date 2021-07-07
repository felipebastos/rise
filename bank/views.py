from django.shortcuts import render
from django.http import HttpResponse

from .models import Donation, Semana
from players.models import Player, Alliance


# Create your views here.
def create_week(request, tag):
    ally = Alliance.objects.filter(tag=tag)[0]

    jogadores = Player.objects.all().exclude(rank='SA').filter(alliance=ally)

    semana = Semana()
    semana.save()

    for jogador in jogadores:
        doacao_programada = Donation()
        doacao_programada.player = jogador
        doacao_programada.semana = semana
        doacao_programada.save()
    
    return HttpResponse(f'Programação para {ally} criada.')