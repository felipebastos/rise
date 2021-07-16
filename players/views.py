import csv
from datetime import date

from django.shortcuts import redirect, render
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required

from .models import Player, PlayerStatus, Alliance, player_status, player_rank, player_spec

# Create your views here.


@login_required
def index(request, game_id):
    try:
        player = Player.objects.get(game_id=game_id)
        status = PlayerStatus.objects.filter(
            player__game_id=game_id).order_by('-data')
        spec = None
        for i, (res, verbose) in enumerate(player_spec):
            if player.specialty == res:
                spec = verbose
        context = {
            'player': player,
            'status': status,
            'spec': spec
        }
    except Player.DoesNotExist:
        raise Http404("Player não encontrado.")
    return render(request, 'players/player.html', context)


@login_required
def edit_player(request, game_id):
    player = Player.objects.filter(game_id=game_id).first()

    allies = Alliance.objects.all()

    if request.method == 'GET':
        context = {
            'player': player,
            'status_list': player_status,
            'ranks_list': player_rank,
            'specialty_list': player_spec,
            'alliances': allies,
        }
        return render(request, 'players/edit.html', context=context)
    player.nick = request.POST['nick']
    player.observacao = request.POST['observacao']
    player.status = request.POST['status']
    player.rank = request.POST['rank']
    player.specialty = request.POST['specialty']
    player.alliance = Alliance.objects.filter(tag=request.POST['ally']).first()
    player.alterado_em = date.today()
    player.alterado_por = request.user
    player.save()
    context = {
        'player': player,
        'status_list': player_status,
        'ranks_list': player_rank,
        'specialty_list': player_spec,
        'alliances': allies,
    }
    return render(request, 'players/edit.html', context=context)

@login_required
def findplayer(request):
    if request.method == 'POST':
        id = request.POST['id']
        return redirect(f'/players/{id}')
    else:
        raise Http404('Só sirvo para buscas do formulário.')

@login_required
def add_status(request, game_id):
    try:
        player = Player.objects.filter(game_id=game_id).first()

        novo_status = PlayerStatus()
        novo_status.player = player
        novo_status.power = request.POST['poder']
        novo_status.killpoints = request.POST['killpoints']
        novo_status.deaths = request.POST['mortes']
        novo_status.save()

        return redirect(f'/players/{game_id}')
    except:
        raise Http404('Player não existe.')


@login_required
def populate(request):
    pass
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
                player=obj_player,
                power=poder,
                killpoints=kills,
                deaths=death
            )
    return HttpResponse('Sucesso! (acho)')


@login_required
def alliance(request, ally_tag):
    try:
        ally = Alliance.objects.filter(tag=ally_tag).first()

        if ally:
            membros = Player.objects.filter(alliance=ally)
            kills = 0
            deaths = 0
            power = 0
            for membro in membros:
                status = PlayerStatus.objects.filter(
                    player=membro).order_by('-data').first()
                if status:
                    kills = kills + status.killpoints
                    deaths = deaths + status.deaths
                    power = power + status.power
            context = {
                'membros': membros,
                'ally': ally,
                'total': len(membros),
                'kills': kills,
                'power': power,
                'death': deaths,
            }
            return render(request, 'players/alianca.html', context)
    except:
        raise Http404('Aliança não está nos registros.')
