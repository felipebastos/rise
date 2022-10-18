import logging
from datetime import date, timedelta

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models.aggregates import Max, Min
from config.models import SiteConfig

from players.models import Advertencia, Player, PlayerStatus

from mge.forms import NovoCriaMGEForm
from mge.models import (
    Comandante,
    EventoDePoder,
    Mge,
    Punido,
    Ranking,
    Inscrito,
    COMMANDERS,
)

from kvk.models import Kvk

# Create your views here.
logger = logging.getLogger("k32")


def index(request):
    mges = Mge.objects.all().order_by("-criado_em")
    form = NovoCriaMGEForm()
    context = {
        "mges": mges,
        "form": form,
    }
    return render(request, "mge/index.html", context=context)


@login_required
def startnew(request):
    form = NovoCriaMGEForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            mge = form.save()
            mge.temporada = (
                Mge.objects.all().aggregate(Max("temporada"))["temporada__max"]
                + 1
            )
            mge.save()
            logger.debug(f"{request.user.username} criou novo MGE {mge}")

    return redirect("/mge/")


def mgeedit(request, mge_id):
    mge = Mge.objects.get(pk=mge_id)

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
    config = SiteConfig.objects.all().first()
    if date.today() > mge.semana() - timedelta(days=config.prazo_inscricao_mge):
        # passou da quinta feira
        insc_encerradas = True
    rank_fechado = False
    if date.today() > mge.semana() + timedelta(days=config.encerra_ranking):
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


def inscrever(request, mge_id):
    mge = Mge.objects.get(pk=mge_id)

    player = Player.objects.filter(game_id=request.POST["player_id"]).first()

    if player and not Inscrito.objects.filter(player=player, mge=mge).first():
        inscrito = Inscrito()
        inscrito.player = player
        inscrito.mge = mge
        inscrito.general = request.POST["general"] or ""

        if "intuito" in request.POST:
            inscrito.intuito = request.POST["intuito"]

        kvk = Kvk.objects.filter(ativo=False).order_by("-inicio").first()

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
        logger.debug(f"Inscrito: {player.game_id} no MGE: {mge}")
    return redirect(f"/mge/view/{mge_id}/")


@login_required
def desinscrever(request, mge_id, player_id):
    mge = Mge.objects.get(pk=mge_id)
    player = Player.objects.filter(game_id=player_id).first()

    aremover = Inscrito.objects.filter(mge=mge).filter(player=player).first()
    aremover.delete()

    return redirect(f"/mge/view/{mge_id}/")


@login_required
def addtorank(request, mge_id, player_id):
    mge = Mge.objects.get(pk=mge_id)
    player = Player.objects.filter(game_id=player_id).first()
    ranking = Ranking()
    ranking.player = player
    ranking.mge = mge
    ranking.save()
    logger.debug(
        f"{request.user.username} adicionou {player.game_id} ao ranking de {mge}"
    )
    return redirect(f"/mge/view/{mge_id}/")


@login_required
def removefromrank(request, mge_id, player_id):
    mge = Mge.objects.get(pk=mge_id)
    player = Player.objects.filter(game_id=player_id).first()

    remover = Ranking.objects.filter(mge=mge).filter(player=player).first()
    remover.delete()
    logger.debug(
        f"{request.user.username} removeu {player.game_id} do ranking de {mge}"
    )

    return redirect(f"/mge/view/{mge_id}/")


@login_required
def punir(request, player_id):
    mge = Mge.objects.order_by("-id").first()
    player = Player.objects.filter(game_id=player_id).first()

    apunir = Punido()
    apunir.mge = mge
    apunir.player = player
    apunir.save()
    logger.debug(f"{request.user.username} puniu {player.game_id} no {mge}")

    adv = Advertencia()
    adv.player = player
    adv.duracao = 15
    adv.descricao = (
        f'Queimou pontuação máxima no {mge} {mge.semana().strftime("%d/%m/%y")}'
    )
    adv.save()

    return redirect(f"/mge/view/{mge.id}/")


@login_required
def despunir(request, mge_id, player_id):
    mge = Mge.objects.get(pk=mge_id)
    player = Player.objects.filter(game_id=player_id).first()

    punicao = Punido.objects.filter(mge=mge).filter(player=player).first()
    punicao.delete()
    logger.debug(
        f"{request.user.username} retirou a punicao de {player.game_id} em {mge}"
    )

    return redirect(f"/mge/view/{mge_id}/")


@login_required
def punir_evento_de_poder(request, player_id):
    player = Player.objects.filter(game_id=player_id).first()

    punicao = EventoDePoder()
    punicao.player = player
    punicao.save()
    logger.debug(
        f"{request.user.username} adicionou punicao a {player.game_id} para evento de poder"
    )

    adv = Advertencia()
    adv.player = player
    adv.duracao = 15
    adv.descricao = f'Quebrou ranking do evento de poder em {timezone.now().strftime("%d/%m/%y")}'
    adv.save()

    return redirect(f"/players/{player_id}/")
