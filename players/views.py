import csv
from datetime import date, datetime

from django.shortcuts import redirect, render
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required

from .models import Player, PlayerStatus, Alliance, player_status, player_rank, player_spec
from kvk.models import Kvk

# Create your views here.


def index(request, game_id):
    try:
        player = Player.objects.get(game_id=game_id)
        status = PlayerStatus.objects.filter(
            player__game_id=game_id).order_by('-data')
        print(status[0])
        spec = None
        for i, (res, verbose) in enumerate(player_spec):
            if player.specialty == res:
                spec = verbose
        temKvk = Kvk.objects.order_by('-inicio').first()
        exibirkvk = False
        if temKvk and temKvk.ativo:
            exibirkvk = True
        context = {
            'player': player,
            'status': status,
            'spec': spec,
            'showkvk': exibirkvk,
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
def listspecs(request, spec):
    players = Player.objects.filter(
        specialty=spec).order_by('alliance')

    specialty = None
    for i, (code, verbose) in enumerate(player_spec):
        if code == spec:
            specialty = verbose

    context = {
        'players': players,
        'spec': specialty,
        'total': len(players),
    }

    return render(request, 'players/spec.html', context=context)


@login_required
def review_players(request, ally_tag):
    if request.method == 'GET':
        try:
            ally = Alliance.objects.filter(tag=ally_tag).first()

            if ally:
                membros = Player.objects.filter(alliance=ally)

                context = {
                    'membros': membros,
                    'ally': ally,
                    'total': len(membros),
                }
                return render(request, 'players/review.html', context)
        except:
            raise Http404('Aliança não está nos registros.')
    else:
        membros = Player.objects.filter(alliance__tag=ally_tag)
        semalianca = Alliance.objects.filter(tag='PSA').first()
        for membro in membros:
            if membro.game_id in request.POST:
                membro.alliance = semalianca
                membro.alterado_por = request.user
                membro.alterado_em = date.today()
                membro.save()
        return redirect(f'/players/review/{ally_tag}/')


def findplayer(request):
    if request.method == 'POST':
        id = request.POST['id']
        return redirect(f'/players/{id}')
    else:
        raise Http404('Só sirvo para buscas do formulário.')


@login_required
def add_status(request, game_id):
    try:
        poder = ''
        if '.' in request.POST['poder']:
            poder = request.POST['poder'].replace('.', '')
        kp = ''
        if '.' in request.POST['killpoints']:
            kp = request.POST['killpoints'].replace('.', '')
        deaths = ''
        if '.' in request.POST['mortes']:
            deaths = request.POST['mortes'].replace('.', '')
        player = Player.objects.filter(game_id=game_id).first()

        novo_status = PlayerStatus()
        novo_status.player = player
        novo_status.power = poder
        novo_status.killpoints = kp
        novo_status.deaths = deaths
        novo_status.save()

        kvk = Kvk.objects.order_by('-inicio').first()
        print(kvk)
        if kvk and kvk.ativo:
            honra = request.POST['honra']
            print(honra)
            zerado = 0
            try:
                if request.POST['zerado']:
                    zerado = 1
            except:
                zerado = 0
            print(zerado)
            return redirect(f'/kvk/update/{kvk.id}/{game_id}/{honra}/{zerado}/')

        return redirect(f'/players/{game_id}/')
    except:
        raise Http404('Player não existe.')


@login_required
def populate(request):
    return Http404('Não mexa aqui')
    with open('/home/k32/rise/dados.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            jogador = Player.objects.filter(game_id=row[0]).first()

            if jogador is None:
                jogador = Player()
                jogador.game_id = row[0]
                jogador.nick = row[1]
                bod = Alliance.objects.filter(tag='BoD').first()
                jogador.alliance = bod
                jogador.save()

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
                player=jogador,
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


@login_required
def top300(request):
    #jogadores = PlayerStatus.objects.all().exclude(player__alliance__tag='MIGR').order_by('-power')[:300]
    jogadores = []
    noreino = Player.objects.exclude(alliance__tag='MIGR')
    for jogador in noreino:
        status = PlayerStatus.objects.filter(
            player=jogador).order_by('-data').first()
        jogadores.append(status)
    jogadores.sort(key=lambda x: x.power if(
        x is not None) else 0, reverse=True)
    poderTotal = 0
    for jogador in jogadores[:300]:
        poderTotal = poderTotal + jogador.power
    context = {
        'jogadores': jogadores[:300],
        'poder': poderTotal,
    }
    return render(request, 'players/top300.html', context=context)


@login_required
def falta_status(request, ally_tag):
    status = PlayerStatus.objects.all()
    id_quem_tem = []
    for cada in status:
        if cada.power != 0:
            id_quem_tem.append(cada.player.id)
    ally = Alliance.objects.filter(tag=ally_tag).first()
    jogadores_sem_status = Player.objects.filter(
        alliance=ally).exclude(id__in=id_quem_tem)

    context = {
        'players': jogadores_sem_status,
    }

    return render(request, 'players/semstatus.html', context=context)


@login_required
def antigos(request, ally_tag):
    status = PlayerStatus.objects.all()
    hoje = date.today()
    id_quem_tem = []
    for cada in status:
        diff = hoje - cada.data
        if diff.days < 15:
            id_quem_tem.append(cada.player.id)
    ally = Alliance.objects.filter(tag=ally_tag).first()
    jogadores_sem_status = Player.objects.filter(
        alliance=ally).exclude(id__in=id_quem_tem)

    context = {
        'players': jogadores_sem_status,
    }

    return render(request, 'players/antigos.html', context=context)


@login_required
def editaStatus(request, status_id):
    if request.method == 'POST':
        status = PlayerStatus.objects.all().filter(id=status_id).first()
        if status.editavel():
            status.power = request.POST['power']
            status.killpoints = request.POST['killpoints']
            status.deaths = request.POST['deaths']
            status.data = datetime.now()
            status.save()

        return redirect(f'/players/{status.player.game_id}')

    status = PlayerStatus.objects.all().filter(id=status_id).first()
    context = {
        'status': status
    }
    return render(request, 'players/editastatus.html', context=context)


@login_required
def delete_status(request, status_id):
    status = PlayerStatus.objects.all().filter(id=status_id).first()
    if status.editavel():
        status.delete()

    return redirect(f'/players/{status.player.game_id}')
