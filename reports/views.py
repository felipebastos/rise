from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Max, Min
from django.shortcuts import render

from datetime import date, datetime, timedelta

from players.models import Alliance, PlayerStatus

# Create your views here.
@login_required
def index(request):
    aliancas = Alliance.objects.all().filter(tag__in=["GoD", "BoD", "AoD"])
    context = {"alliances": aliancas}

    if request.method == "POST":
        try:
            universo = request.POST["universo"]
            inicio = request.POST["inicio"]
            fim = request.POST["fim"]
            ordem = request.POST["ordem"]

            context["inicio"] = date.fromisoformat(inicio)
            context["fim"] = date.fromisoformat(fim)

            ord = ""
            if ordem == "kp":
                ord = "-kp"
                context["titulo"] = f"Ranking por Killpoints de {universo}"
            else:
                ord = "-dt"
                context["titulo"] = f"Ranking por Mortes de {universo}"

            status = None
            if universo == "K32":
                status = (
                    PlayerStatus.objects.all()
                    .filter(data__gte=inicio)
                    .filter(data__lte=fim)
                    .values("player__nick")
                    .annotate(
                        kp=Max("killpoints") - Min("killpoints"),
                        dt=Max("deaths") - Min("deaths"),
                    )
                    .order_by(ord)
                )
            else:
                status = (
                    PlayerStatus.objects.all()
                    .filter(player__alliance__tag=universo)
                    .filter(data__gte=inicio)
                    .filter(data__lte=fim)
                    .values("player__nick")
                    .annotate(
                        kp=Max("killpoints") - Min("killpoints"),
                        dt=Max("deaths") - Min("deaths"),
                    )
                    .order_by(ord)
                )

            context["rank"] = status
        except Exception:
            pass

    return render(request, "reports/index.html", context=context)


@login_required
def top300(request):
    ultimo = PlayerStatus.objects.order_by("-data").first()

    oReino = (
        PlayerStatus.objects.exclude(player__alliance__tag="MIGR")
        .exclude(player__status="INATIVO")
        .filter(
            data__year=ultimo.data.year,
            data__month=ultimo.data.month,
            data__day=ultimo.data.day,
        )
        .order_by("-power")
    )

    poder_de_batalha = 0
    poder_de_sacrificio = 0
    for p in oReino:
        if p.player.status not in ["FARM", "BANIDO"]:
            poder_de_batalha += p.power
        if p.player.status not in ["BANIDO"]:
            poder_de_sacrificio += p.power

    os300 = oReino[:300]

    poder = 0
    for p in os300:
        poder += p.power

    context = {
        "jogadores": os300,
        "poder": poder,
        "p_batalha": poder_de_batalha,
        "p_sacrificio": poder_de_sacrificio,
    }
    return render(request, "reports/top300.html", context=context)


@login_required
def top300rev(request):
    oReino = (
        PlayerStatus.objects.exclude(player__alliance__tag="MIGR")
        .exclude(player__status="INATIVO")
        .order_by("-data")
    )

    oReinoUnico = {}
    for status in oReino:
        if status.player.game_id not in oReinoUnico.keys():
            oReinoUnico[status.player.game_id] = status

    todos = list(oReinoUnico.values())
    todos.sort(key=lambda x: x.power if (x is not None) else 0, reverse=True)

    os300 = todos[:300]

    context = {
        "jogadores": os300,
    }

    return render(request, "reports/rev300.html", context=context)
