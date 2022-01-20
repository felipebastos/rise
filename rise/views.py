from django.db.models.aggregates import Count, Max
from django.db.models.expressions import Case, When
from players.models import Alliance, PlayerStatus, Player
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from datetime import datetime, timezone, timedelta

from .forms import LoginForm

def index(request):
    hoje = datetime.now(timezone(timedelta(hours=-3)))

    players_god = Player.objects.filter(alliance__tag='GoD')
    god_atrasados = 0
    god_nulos = 0
    for player in players_god:
        status = PlayerStatus.objects.filter(
            player=player).order_by('-data').first()
        if status:
            delta = hoje - status.data
            if delta.days > 15:
                god_atrasados = god_atrasados + 1
            if status.power == 0:
                god_nulos = god_nulos + 1
        else:
            god_nulos = god_nulos + 1
    players_bod = Player.objects.filter(alliance__tag='BoD')
    bod_atrasados = 0
    bod_nulos = 0
    for player in players_bod:
        status = PlayerStatus.objects.filter(
            player=player).order_by('-data').first()
        if status:
            delta = hoje - status.data
            if delta.days > 15:
                bod_atrasados = bod_atrasados + 1
            if status.power == 0:
                bod_nulos = bod_nulos + 1
        else:
            bod_nulos = bod_nulos + 1

    context = {
        'god_antigos': god_atrasados,
        'god_nulos': god_nulos,
        'bod_antigos': bod_atrasados,
        'bod_nulos': bod_nulos,
    }

    return render(request, 'rise/index.html', context=context)


def logar(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                # Return an 'invalid login' error message.
                return redirect('/login')
    form = LoginForm()
    context = {
        'form': form,
    }
    return render(request, 'rise/login.html', context=context)


@login_required
def sair(request):
    logout(request)
    return redirect('/')
