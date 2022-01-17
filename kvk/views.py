from datetime import date

from django.shortcuts import redirect, render
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Max, Min
from django.utils import timezone

from players.models import Player, PlayerStatus

from .models import Kvk, Zerado
# Create your views here.


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

    return redirect('/kvk/')



def show_kvk(request, kvkid):
    kvk = Kvk.objects.filter(id=kvkid).first()
    
    zerados = Zerado.objects.filter(kvk=kvk)
    zerados_lista = []
    for zerado in zerados:
        zerados_lista.append(zerado.player)

    final = kvk.final
    if not final:
        final = timezone.now()

    topkp = PlayerStatus.objects.all().exclude(player__in=zerados_lista).filter(data__gte=kvk.inicio).filter(data__lte=final).values('player__nick').annotate(kp=Max('killpoints')-Min('killpoints'), dt=Max('deaths')-Min('deaths')).order_by('-kp')[0:10]
    topdt = PlayerStatus.objects.all().exclude(player__in=zerados_lista).filter(data__gte=kvk.inicio).filter(data__lte=final).values('player__nick').annotate(kp=Max('killpoints')-Min('killpoints'), dt=Max('deaths')-Min('deaths')).order_by('-dt')[0:10]

    context = {
        'kvk': kvk,
        'zerados': zerados,
        'topkp': topkp,
        'topdt': topdt,
    }
    return render(request, 'kvk/kvk.html', context=context)


@login_required
def close_kvk(request, kvk_id):
    kvk = Kvk.objects.get(pk=kvk_id)
    kvk.ativo = not kvk.ativo
    kvk.save()
    return redirect(f'/kvk/edit/{kvk_id}/')


@login_required
def add_zerado(request, player_id):
    running_kvk = Kvk.objects.filter(ativo=True).first()

    if running_kvk:
        quem = Player.objects.filter(game_id=player_id).first()
        zerado = Zerado()
        zerado.player = quem
        zerado.kvk = running_kvk
        zerado.save()
        return redirect(f'/kvk/edit/{running_kvk.id}/')
    
    return Http404('Não há kvk em andamento.')

@login_required
def removezerado(request, kvk, zerado_id):
    zerado = Zerado.objects.get(pk=zerado_id)
    zerado.delete()

    return redirect(f'/kvk/edit/{zerado.kvk.id}/')