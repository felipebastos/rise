from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Player, PlayerStatus, Alliance

import csv

# Create your views here.

def index(request, game_id):
    try:
        player = Player.objects.get(game_id=game_id)
        status = PlayerStatus.objects.filter(player__game_id=game_id).order_by('-data')
        context = {
            'player': player,
            'status': status
            }
    except Player.DoesNotExist:
        raise Http404("Player não encontrado.")
    return render(request, 'players/player.html', context)

def populate(request):
    with open('/home/k32/rise/dados.csv') as f:
        reader = csv.reader(f)
        ally = Alliance.objects.filter(tag='AoD')[0]
        for row in reader:
            obj_player, created_player = Player.objects.get_or_create(
                game_id=row[0],
                nick=row[1],
                alliance=ally
                )
            poder = row[2]
            if row[2] == '':
                poder = 0

            kills = row[3]
            if row[3] == '':
                kills = 0

            death = row[4]
            if row[4] == '':
                death = 0

            obj_status, created_status = PlayerStatus.objects.get_or_create(
                player = obj_player,
                power = poder,
                killpoints = kills,
                deaths = death
                )
    return HttpResponse('Sucesso! (acho)')

def alliance(request, ally_tag):
    ally = Alliance.objects.filter(tag=ally_tag)[0]

    if ally:
        membros = Player.objects.filter(alliance=ally).exclude(status='SA')
        context = {
            'membros': membros,
            'ally': ally,
            'total': len(membros)
        }
        return render(request, 'players/alianca.html', context)
    else:
        return Http404('Aliança não está nos registros.')
