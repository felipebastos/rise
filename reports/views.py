from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Max, Min
from django.shortcuts import render
from django.core.paginator import Paginator

from datetime import date, datetime, timedelta, timezone

from players.models import Alliance, PlayerStatus, Player
from rise.forms import SearchPlayerForm

# Create your views here.
@login_required
def index(request):
    hoje = datetime.now(timezone(timedelta(hours=-3)))

    god_atrasados = 0
    god_nulos = 0
    bod_atrasados = 0
    bod_nulos = 0

    if request.user.is_authenticated:
        players_god = Player.objects.filter(alliance__tag="GoD")

        for player in players_god:
            status = (
                PlayerStatus.objects.filter(player=player)
                .order_by("-data")
                .first()
            )
            if status:
                delta = hoje - status.data
                if delta.days > 15:
                    god_atrasados = god_atrasados + 1
                if status.power == 0:
                    god_nulos = god_nulos + 1
            else:
                god_nulos = god_nulos + 1
        players_bod = Player.objects.filter(alliance__tag="BoD")

        for player in players_bod:
            status = (
                PlayerStatus.objects.filter(player=player)
                .order_by("-data")
                .first()
            )
            if status:
                delta = hoje - status.data
                if delta.days > 15:
                    bod_atrasados = bod_atrasados + 1
                if status.power == 0:
                    bod_nulos = bod_nulos + 1
            else:
                bod_nulos = bod_nulos + 1

    aliancas = Alliance.objects.all().filter(tag__in=["GoD", "BoD", "AoD"])

    searchform = SearchPlayerForm()

    context = {
        "searchform": searchform,
        "god_antigos": god_atrasados,
        "god_nulos": god_nulos,
        "bod_antigos": bod_atrasados,
        "bod_nulos": bod_nulos,
        "alliances": aliancas,
    }

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

    paginator = Paginator(os300, 25)

    page_number = request.GET.get("page")

    pagina = paginator.get_page(page_number)

    poder = 0
    for p in os300:
        poder += p.power

    slice = 0
    if page_number:
        slice = (int(page_number) - 1) * 25

    context = {
        "jogadores": pagina,
        "poder": poder,
        "p_batalha": poder_de_batalha,
        "p_sacrificio": poder_de_sacrificio,
        "range": range(1, pagina.paginator.num_pages + 1),
        "slice": slice,
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
