from players.models import PlayerStatus
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, SearchPlayerForm


def ang(request):
    return render(request, "rise/ang.html")


def index(request):
    ultimo = PlayerStatus.objects.order_by("-data").first()

    oReinoPoder = (
        PlayerStatus.objects.exclude(player__alliance__tag="MIGR")
        .exclude(player__status="INATIVO")
        .exclude(player__status="BANIDO")
        .filter(
            data__year=ultimo.data.year,
            data__month=ultimo.data.month,
            data__day=ultimo.data.day,
        )
        .order_by("-power")
    )

    oReinokillpoints = (
        PlayerStatus.objects.exclude(player__alliance__tag="MIGR")
        .exclude(player__status="INATIVO")
        .exclude(player__status="BANIDO")
        .filter(
            data__year=ultimo.data.year,
            data__month=ultimo.data.month,
            data__day=ultimo.data.day,
        )
        .order_by("-killpoints")
    )

    oReinomortes = (
        PlayerStatus.objects.exclude(player__alliance__tag="MIGR")
        .exclude(player__status="INATIVO")
        .exclude(player__status="BANIDO")
        .filter(
            data__year=ultimo.data.year,
            data__month=ultimo.data.month,
            data__day=ultimo.data.day,
        )
        .order_by("-deaths")
    )

    context = {
        "top10poder": oReinoPoder[:10],
        "top10kp": oReinokillpoints[:10],
        "top10dt": oReinomortes[:10],
    }

    return render(request, "rise/index.html", context=context)


def logar(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                # Return an 'invalid login' error message.
                return redirect("/login")
    form = LoginForm()
    context = {
        "form": form,
    }
    return render(request, "rise/login.html", context=context)


@login_required
def sair(request):
    logout(request)
    return redirect("/")
