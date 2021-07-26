from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import date
from players.models import Player
from .models import Mge, Punido, Ranking, Inscrito
from kvk.models import Kvk, Desempenho

# Create your views here.


def index(request):
    mges = Mge.objects.all()
    context = {
        'mges': mges,
    }
    return render(request, 'mge/index.html', context=context)


@login_required
def startnew(request):
    mge = Mge()
    mge.save()
    return redirect('/mge/')


def mgeedit(request, id):
    mge = Mge.objects.filter(id=id).first()
    inscritos = Inscrito.objects.filter(mge=mge).order_by('inserido')
    id_inscritos = []
    for inscrito in inscritos:
        id_inscritos.append(inscrito.player.id)
    ultimo_kvk = Kvk.objects.filter(inicio__lte=mge.criado_em).filter(ativo=False).order_by('-inicio').first()
    desempenho_inscritos = Desempenho.objects.filter(kvk=ultimo_kvk).filter(player__in=id_inscritos)
    
    if ultimo_kvk is None:
        desempenho_inscritos = inscritos
    rank = Ranking.objects.filter(mge=mge).order_by('inserido')
    punidos = Punido.objects.filter(mge=mge).order_by('inserido')
    insc_encerradas = False
    if date.today() > mge.semana() and date.today().weekday() > 3:
        # passou da quinta feira
        insc_encerradas = True
    rank_fechado = False
    if date.today() > mge.semana():
        rank_fechado = True
    context = {
        'mge': mge,
        'inscritos': desempenho_inscritos,
        'insc_encerradas': insc_encerradas,
        'rank': rank,
        'rank_fechado': rank_fechado,
        'punidos': punidos,
    }
    return render(request, 'mge/mge.html', context=context)


@login_required
def inscrever(request, id):
    mge = Mge.objects.filter(id=id).first()
    player = Player.objects.filter(game_id=request.POST['player_id']).first()
    inscrito = Inscrito()
    inscrito.player = player
    inscrito.mge = mge
    inscrito.save()
    return redirect(f'/mge/editar/{id}/')


@login_required
def desinscrever(request, id, player_id):
    mge = Mge.objects.filter(id=id).first()
    player = Player.objects.filter(game_id=player_id).first()

    aremover = Inscrito.objects.filter(mge=mge).filter(player=player).first()
    aremover.delete()

    return redirect(f'/mge/editar/{id}/')


@login_required
def addtorank(request, id, player_id):
    mge = Mge.objects.filter(id=id).first()
    player = Player.objects.filter(game_id=player_id).first()
    ranking = Ranking()
    ranking.player = player
    ranking.mge = mge
    ranking.save()
    return redirect(f'/mge/editar/{id}/')


@login_required
def removefromrank(request, id, player_id):
    mge = Mge.objects.filter(id=id).first()
    player = Player.objects.filter(game_id=player_id).first()

    remover = Ranking.objects.filter(mge=mge).filter(player=player).first()
    remover.delete()

    return redirect(f'/mge/editar/{id}/')


@login_required
def punir(request, player_id):
    mge = Mge.objects.order_by('-id').first()
    player = Player.objects.filter(game_id=player_id).first()

    apunir = Punido()
    apunir.mge = mge
    apunir.player = player
    apunir.save()

    return redirect(f'/mge/editar/{mge.id}/')

@login_required
def despunir(request, id, player_id):
    mge = Mge.objects.filter(id=id).first()
    player = Player.objects.filter(game_id=player_id).first()

    despunir = Punido.objects.filter(mge=mge).filter(player=player).first()
    despunir.delete()

    return redirect(f'/mge/editar/{id}/')