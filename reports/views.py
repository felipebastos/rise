from datetime import date, datetime, timedelta, timezone

from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Max, Min
from django.shortcuts import render
from django.core.paginator import Paginator

from players.models import PLAYER_STATUS, Alliance, PlayerStatus, Player
from kvk.models import faixas
from reports.forms import FiltroForm
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
        principal = Alliance.objects.get(pk=1)
        players_god = Player.objects.filter(alliance=principal)

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

        secundaria = Alliance.objects.get(pk=2)
        players_bod = Player.objects.filter(alliance=secundaria)

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

    aliancas = Alliance.objects.all().filter(tag__in=["32BR", "32br", "AoD"])

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
        universo = request.POST["universo"]
        inicio = request.POST["inicio"]
        fim = request.POST["fim"]
        ordem = request.POST["ordem"]

        context["inicio"] = date.fromisoformat(inicio)
        context["fim"] = date.fromisoformat(fim)

        ordem = ""
        if ordem == "kp":
            ordem = "-kp"
            context["titulo"] = f"Ranking por Killpoints de {universo}"
        else:
            ordem = "-dt"
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
                .order_by(ordem)
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
                .order_by(ordem)
            )

        context["rank"] = status

    return render(request, "reports/index.html", context=context)


@login_required
def busca_especial(request):
    form = FiltroForm(initial={"poder_max": "200000000"})
    minimo = 0
    maximo = 2000000000
    order = "power"
    aliancas = Alliance.objects.all()
    status = [item[0] for item in PLAYER_STATUS]
    ultimo_dia = PlayerStatus.objects.all().order_by("-data").first().data
    if request.method == "POST":
        form = FiltroForm(request.POST or None)

        if form.is_valid():
            if int(form.cleaned_data.get("poder_max")) > int(
                form.cleaned_data.get("poder_min")
            ):
                minimo = int(form.cleaned_data.get("poder_min"))
                maximo = int(form.cleaned_data.get("poder_max"))
            if "order" in form.cleaned_data:
                order = form.cleaned_data.get("order")

            if form.cleaned_data.get("alianca"):
                aliancas = form.cleaned_data.get("alianca")

            if form.cleaned_data.get("status"):
                status = form.cleaned_data.get("status")

    ultimos = (
        PlayerStatus.objects.filter(
            data__year=ultimo_dia.year,
            data__month=ultimo_dia.month,
            data__day=ultimo_dia.day,
        )
        .filter(player__alliance__in=aliancas)
        .filter(player__status__in=status)
        .filter(power__gte=minimo, power__lte=maximo)
        .order_by(f"-{order}")
    )

    contexto = {
        "form": form,
        "resultado": ultimos,
    }
    return render(request, "reports/buscaespecial.html", context=contexto)


@login_required
def top300(request):
    ultimo = PlayerStatus.objects.order_by("-data").first()

    o_reino = (
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
    for status in o_reino:
        if status.player.status not in ["FARM", "BANIDO"]:
            poder_de_batalha += status.power
        if status.player.status not in ["BANIDO"]:
            poder_de_sacrificio += status.power

    os300 = o_reino[:300]

    paginator = Paginator(os300, 25)

    page_number = request.GET.get("page")

    pagina = paginator.get_page(page_number)

    poder = 0
    for status in os300:
        poder += status.power

    fatia = 0
    if page_number:
        fatia = (int(page_number) - 1) * 25

    context = {
        "jogadores": pagina,
        "poder": poder,
        "p_batalha": poder_de_batalha,
        "p_sacrificio": poder_de_sacrificio,
        "range": range(1, pagina.paginator.num_pages + 1),
        "slice": fatia,
    }
    return render(request, "reports/top300.html", context=context)


def analisedesempenho(request, cat):
    if cat not in ["kp", "dt"]:
        return render(request, "rise/404.html")

    ultima_leitura = PlayerStatus.objects.order_by("-data").first()
    banidos_e_inativos = Player.objects.filter(
        status__in=["BANIDO", "MIGROU", "INATIVO"]
    )

    o_reino = (
        PlayerStatus.objects.exclude(player__alliance__tag="MIGR")
        .exclude(player__status="INATIVO")
        .filter(
            data__year=ultima_leitura.data.year,
            data__month=ultima_leitura.data.month,
            data__day=ultima_leitura.data.day,
        )
        .order_by("-power")
    )

    o_reino_unico = {}
    for status in o_reino:
        if status.player.game_id not in o_reino_unico:
            o_reino_unico[status.player.game_id] = status

    todos = list(o_reino_unico.values())
    todos.sort(key=lambda x: x.power if (x is not None) else 0, reverse=True)

    os300 = todos[:300]

    mais_fraco_do_top300 = os300[-1:]

    context = {
        "tipo": cat,
    }

    categorizados = []
    for faixa in faixas:
        faixa_original = (
            PlayerStatus.objects.filter(
                power__gte=mais_fraco_do_top300[0].power
            )
            .filter(
                data__year=ultima_leitura.data.year,
                data__month=ultima_leitura.data.month,
                data__day=ultima_leitura.data.day,
                power__gte=faixa[0],
                power__lte=faixa[1],
            )
            .order_by("data")
        )

        players_faixa_original = []
        for stat in faixa_original:
            if stat.player not in players_faixa_original:
                if stat.data.hour == ultima_leitura.data.hour:
                    players_faixa_original.append(stat.player)

        status = (
            PlayerStatus.objects.exclude(player__in=banidos_e_inativos)
            .filter(player__in=players_faixa_original)
            .filter(
                data__year=ultima_leitura.data.year,
                data__month=ultima_leitura.data.month,
                data__day=ultima_leitura.data.day,
            )
            .values("player__nick", "player__game_id", "player__alliance__tag")
            .annotate(
                kp=Max("killpoints"),
                dt=Max("deaths"),
            )
            .order_by(f"-{cat}")
        )
        media = 0
        if len(status) > 0:
            for stat in status:
                media = media + stat[cat]

            media = media // len(status)

        categorizados.append(
            {
                "faixa0": faixa[0],
                "faixa1": faixa[1],
                "media": media,
                "meiamedia": media * 0.5,
                "membros": status,
            }
        )
        context["categorizados"] = categorizados

    return render(request, "reports/analise.html", context=context)
