from datetime import date

from django.shortcuts import redirect, render
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required

from .models import Kvk, Desempenho
from players.models import Player, Alliance, PlayerStatus
# Create your views here.


@login_required
def index(request):
    kvks = Kvk.objects.all().order_by('-inicio')
    context = {
        'kvks': kvks,
    }
    return render(request, 'kvk/index.html', context=context)


@login_required
def new_kvk(request):
    novo = Kvk()
    novo.inicio = request.POST['inicio']
    novo.save()

    players = Player.objects.all().filter(
        alliance__tag__in=['GoD', 'BoD', 'AoD'])
    for player in players:
        status = PlayerStatus.objects.filter(
            player=player).order_by('-data').first()
        if status:
            novo_desempenho = Desempenho()
            novo_desempenho.kvk = novo
            novo_desempenho.player = player
            novo_desempenho.primeiro_status = status
            novo_desempenho.ultimo_status = status
            novo_desempenho.save()
    return redirect('/kvk/')


@login_required
def show_kvk(request, kvk_id):
    kvk = Kvk.objects.filter(id=kvk_id).first()
    desempenhos = Desempenho.objects.filter(kvk=kvk).order_by('player__nick')
    context = {
        'kvk': kvk,
        'desempenhos': desempenhos,
    }
    return render(request, 'kvk/kvk.html', context=context)


@login_required
def milestone_kvk(request, kvk_id, player_id, honra, zerado):
    kvk = Kvk.objects.filter(id=kvk_id).first()
    player = Player.objects.filter(game_id=player_id).first()
    desempenho = Desempenho.objects.filter(
        kvk=kvk).filter(player=player).first()
    if desempenho:
        status = PlayerStatus.objects.filter(
            player=player).order_by('-data').first()
        desempenho.ultimo_status = status
        desempenho.zerado = zerado
        desempenho.honra = honra
        desempenho.save()
    return redirect(f'/players/{player_id}/')


@login_required
def close_kvk(request, kvk_id):
    kvk = Kvk.objects.filter(id=kvk_id).first()
    kvk.ativo = not kvk.ativo
    kvk.save()
    return redirect(f'/kvk/edit/{kvk_id}/')
