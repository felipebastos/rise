from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models.aggregates import Max, Min
from datetime import date, timedelta
from mge.forms import COMMANDERS, CriaMGE
from players.models import Player, PlayerStatus
from .models import Comandante, EventoDePoder, Mge, Punido, Ranking, Inscrito
from kvk.models import Kvk

# Create your views here.


def index(request):
    mges = Mge.objects.all().order_by("-criado_em")
    form = CriaMGE()
    context = {
        "mges": mges,
        "form": form,
    }
    return render(request, "mge/index.html", context=context)


@login_required
def startnew(request):
    form = CriaMGE(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            quais = form.cleaned_data.get("commanders")
            mge = Mge()
            mge.tipo = quais
            mge.save()

    return redirect("/mge/")


def mgeedit(request, id):
    mge = Mge.objects.filter(id=id).first()

    opcoes = None
    if 0 < int(mge.tipo) < 5:
        opcoes = COMMANDERS[int(mge.tipo) - 1]
    if int(mge.tipo) >= 5:
        opcoes = COMMANDERS[int(mge.tipo) - 5]
        if "Lançamento" not in opcoes:
            opcoes.append("Lançamento")

    generais = Comandante.objects.filter(tipo=mge.tipo_mge)

    inscritos = Inscrito.objects.filter(mge=mge).order_by("inserido")

    rank = Ranking.objects.filter(mge=mge).order_by("inserido")
    punidos = Punido.objects.filter(mge=mge).order_by("inserido")
    insc_encerradas = False
    if date.today() > mge.semana() - timedelta(days=3):
        # passou da quinta feira
        insc_encerradas = True
    rank_fechado = False
    if date.today() > mge.semana() + timedelta(days=4):
        rank_fechado = True
    context = {
        "mge": mge,
        "opcoes": opcoes,
        "generais": generais,
        "insc_encerradas": insc_encerradas,
        "rank": rank,
        "rank_fechado": rank_fechado,
        "punidos": punidos,
        "inscritos": inscritos,
    }
    return render(request, "mge/mge.html", context=context)


def inscrever(request, id):
    mge = Mge.objects.filter(id=id).first()

    player = Player.objects.filter(game_id=request.POST["player_id"]).first()

    if player and not Inscrito.objects.filter(player=player, mge=mge).first():
        inscrito = Inscrito()
        inscrito.player = player
        inscrito.mge = mge
        inscrito.general = request.POST["general"] or ""

        kvk = Kvk.objects.order_by("-inicio").first()

        final = kvk.final
        if not final:
            final = timezone.now()

        status = (
            PlayerStatus.objects.all()
            .filter(player=player)
            .filter(data__gte=kvk.inicio)
            .filter(data__lte=final)
            .values("player__nick")
            .annotate(
                kp=Max("killpoints") - Min("killpoints"),
                dt=Max("deaths") - Min("deaths"),
            )
        )

        if status:
            inscrito.kills = status[0]["kp"]
            inscrito.deaths = status[0]["dt"]
        else:
            inscrito.kills = -1
            inscrito.deaths = -1

        inscrito.save()
    return redirect(f"/mge/view/{id}/")


@login_required
def desinscrever(request, id, player_id):
    mge = Mge.objects.filter(id=id).first()
    player = Player.objects.filter(game_id=player_id).first()

    aremover = Inscrito.objects.filter(mge=mge).filter(player=player).first()
    aremover.delete()

    return redirect(f"/mge/view/{id}/")


@login_required
def addtorank(request, id, player_id):
    mge = Mge.objects.filter(id=id).first()
    player = Player.objects.filter(game_id=player_id).first()
    ranking = Ranking()
    ranking.player = player
    ranking.mge = mge
    ranking.save()
    return redirect(f"/mge/view/{id}/")


@login_required
def removefromrank(request, id, player_id):
    mge = Mge.objects.filter(id=id).first()
    player = Player.objects.filter(game_id=player_id).first()

    remover = Ranking.objects.filter(mge=mge).filter(player=player).first()
    remover.delete()

    return redirect(f"/mge/view/{id}/")


@login_required
def punir(request, player_id):
    mge = Mge.objects.order_by("-id").first()
    player = Player.objects.filter(game_id=player_id).first()

    apunir = Punido()
    apunir.mge = mge
    apunir.player = player
    apunir.save()

    return redirect(f"/mge/view/{mge.id}/")


@login_required
def despunir(request, id, player_id):
    mge = Mge.objects.filter(id=id).first()
    player = Player.objects.filter(game_id=player_id).first()

    despunir = Punido.objects.filter(mge=mge).filter(player=player).first()
    despunir.delete()

    return redirect(f"/mge/view/{id}/")


@login_required
def punirEventoDePoder(request, playerId):
    player = Player.objects.filter(game_id=playerId).first()

    punicao = EventoDePoder()
    punicao.player = player
    punicao.save()

    return redirect(f"/players/{playerId}/")