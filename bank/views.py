from django.http.response import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from datetime import date, timedelta

from .models import Donation, Semana
from players.models import Player, Alliance


# Create your views here.
@login_required
def index(request):
    semanas = Semana.objects.all()
    context = {
        'semanas': semanas
    }

    return render(request, 'bank/index.html', context=context)


@login_required
def create_week(request, tag, resource):
    ally = Alliance.objects.filter(tag=tag)[0]

    jogadores = Player.objects.all().exclude(rank='SA').filter(alliance=ally)

    semana = Semana()
    semana.recurso = resource
    semana.save()

    for jogador in jogadores:
        doacao_programada = Donation()
        doacao_programada.player = jogador
        doacao_programada.semana = semana
        doacao_programada.save()

    return redirect('/bank/')


@login_required
def week(request, weekid):
    semana = Semana.objects.get(id=weekid)

    doadores = Donation.objects.filter(
        semana=semana).order_by('player__game_id')

    context = {
        'semana': semana,
        'doadores': doadores,
    }

    return render(request, 'bank/week.html', context=context)


@login_required
def donated(request, donationid):
    doador = Donation.objects.get(id=donationid)

    doador.donated = not doador.donated

    doador.save()

    return redirect(f'/bank/week/{doador.semana.id}')


@login_required
def donations_report(request):
    context = {
        'devedores': Donation.objects.filter(donated=False).order_by('player')
    }
    return render(request, 'bank/report.html', context=context)
