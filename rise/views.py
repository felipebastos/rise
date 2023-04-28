from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from config.models import SiteConfig
from players.models import PlayerStatus
from rise.forms import LoginForm


def index(request):
    ultimo = PlayerStatus.objects.order_by("-data").first()

    o_reino_poder = (
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

    o_reino_killpoints = (
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

    o_reino_mortes = (
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

    config = SiteConfig.objects.all().first()

    context = {
        "top10poder": o_reino_poder[:10],
        "top10kp": o_reino_killpoints[:10],
        "top10dt": o_reino_mortes[:10],
        "config": config,
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
