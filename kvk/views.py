import csv
import logging
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db.models.aggregates import Max, Min
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.utils import timezone

from kvk.forms import (
    CargoForm,
    EtapaForm,
    KvkConfigForm,
    KvKStatusForm,
    UploadEtapasFileForm,
)
from kvk.models import (
    AdicionalDeFarms,
    Batalha,
    Cargo,
    Consolidado,
    Etapas,
    Kvk,
    KvKStatus,
    PontosDeMGE,
    Zerado,
    faixas,
)
from players.forms import UploadFileForm
from players.models import Player, PlayerStatus

# Create your views here.
logger = logging.getLogger("k32")


def index(request):
    kvks = Kvk.objects.all().order_by("-inicio")
    context = {
        "kvks": kvks,
    }
    return render(request, "kvk/index.html", context=context)


@login_required
def new_kvk(request):
    novo = Kvk()
    novo.inicio = request.POST["inicio"]
    novo.save()
    logger.debug("%s criou novo kvk: %s", request.user.username, novo)

    return redirect("/kvk/")


def show_kvk(request, kvkid):
    kvk = Kvk.objects.filter(id=kvkid).first()

    zerados = Zerado.objects.filter(kvk=kvk)
    zerados_lista = []
    for zerado in zerados:
        zerados_lista.append(zerado.player)

    inicio = kvk.inicio
    if kvk.primeira_luta:
        inicio = kvk.primeira_luta

    final = kvk.final
    if not final:
        final = timezone.now()

    farms_banidos_e_inativos = Player.objects.filter(
        status__in=["BANIDO", "FARM", "MIGROU", "INATIVO"]
    )

    topkp = (
        PlayerStatus.objects.all()
        .exclude(player__in=farms_banidos_e_inativos)
        .filter(data__gte=inicio)
        .filter(data__lte=final)
        .values("player__nick", "player__game_id")
        .annotate(
            kp=Max("killpoints") - Min("killpoints"),
            dt=Max("deaths") - Min("deaths"),
        )
        .order_by("-kp")[0:10]
    )
    topdt = (
        PlayerStatus.objects.all()
        .exclude(player__in=zerados_lista)
        .exclude(player__in=farms_banidos_e_inativos)
        .filter(data__gte=inicio)
        .filter(data__lte=final)
        .values("player__nick", "player__game_id")
        .annotate(
            kp=Max("killpoints") - Min("killpoints"),
            dt=Max("deaths") - Min("deaths"),
        )
        .order_by("-dt")[0:10]
    )

    context = {
        "kvk": kvk,
        "zerados": zerados,
        "topkp": topkp,
        "topdt": topdt,
    }
    return render(request, "kvk/kvk.html", context=context)


@login_required
def close_kvk(request, kvk_id):
    kvk = Kvk.objects.get(pk=kvk_id)
    kvk.ativo = not kvk.ativo
    kvk.final = timezone.now()
    kvk.save()
    logger.debug("%s abriu/fechou %s", request.user.username, kvk)
    return redirect(f"/kvk/edit/{kvk_id}/")


@login_required
def add_zerado(request, player_id):
    running_kvk = Kvk.objects.filter(ativo=True).first()

    if running_kvk:
        quem = Player.objects.filter(game_id=player_id).first()
        zerado = Zerado()
        zerado.player = quem
        zerado.kvk = running_kvk
        zerado.save()
        logger.debug(
            "%s marcou %s como zerado em %s",
            request.user.username,
            quem.game_id,
            running_kvk,
        )
        return redirect(f"/kvk/edit/{running_kvk.id}/")

    return render(request, "rise/404.html")


@login_required
def removezerado(request, kvk, zerado_id):
    zerado = Zerado.objects.get(pk=zerado_id)
    if kvk == zerado.kvk.id:
        player = zerado.player
        zerado.delete()
        logger.debug(
            "%s removeu %s dos zerados.", request.user.username, player.game_id
        )

    return redirect(f"/kvk/edit/{zerado.kvk.id}/")


def calcular(kvk, cat):
    abates_de_zerado = {}

    inicio = kvk.inicio
    if kvk.primeira_luta:
        inicio = kvk.primeira_luta

    final = kvk.final
    if not final:
        final = timezone.now()

    context = {
        "tipo": cat,
        "kvk": kvk.id,
    }

    contexto = cache.get(f"context_{cat}_{kvk.id}")

    if contexto:
        return contexto

    if "zerados" not in context:
        banidos_e_inativos = Player.objects.filter(status__in=["BANIDO", "INATIVO"])
        banidos_inativos_ids = []
        for player in banidos_e_inativos:
            banidos_inativos_ids.append(player.id)

        primeiro = (
            PlayerStatus.objects.filter(data__gte=kvk.inicio).order_by("data").first()
        )

        if not primeiro:
            return redirect(f"/kvk/edit/{kvk.id}/")

        zerados = Zerado.objects.filter(kvk=kvk)
        zerados_lista = []
        zerados_ids = []
        for zerado_pra_lista in zerados:
            zerados_lista.append(zerado_pra_lista.player)
            zerados_ids.append(zerado_pra_lista.player.id)

        farms = Player.objects.filter(status__in=["FARM"])
        farms_ids = []
        for player in farms:
            farms_ids.append(player.id)

        context["zerados"] = zerados_ids
        context["banidos_inativos"] = banidos_inativos_ids
        context["farms"] = farms_ids

        categorizados = []
        for faixa in faixas:
            faixa_original = PlayerStatus.objects.filter(
                data__year=primeiro.data.year,
                data__month=primeiro.data.month,
                data__day=primeiro.data.day,
                power__gte=faixa[0],
                power__lte=faixa[1],
            ).order_by("data")

            players_faixa_original = []
            for stat in faixa_original:
                if stat.player not in players_faixa_original:
                    if stat.data.hour == primeiro.data.hour:
                        players_faixa_original.append(stat.player)

            batalhas = Batalha.objects.filter(kvk=kvk)

            status = None
            if batalhas:
                acumulado = []
                for batalha in batalhas:
                    por_batalha = (
                        PlayerStatus.objects.filter(player__in=players_faixa_original)
                        .filter(data__gte=batalha.data_inicio)
                        .filter(data__lte=batalha.data_fim)
                        .values(
                            "player",
                            "player__nick",
                            "player__game_id",
                            "player__alliance__tag",
                        )
                        .annotate(
                            kp=Max("killpoints") - Min("killpoints"),
                            dt=Max("deaths") - Min("deaths"),
                        )
                        .order_by(f"-{cat}")
                    )
                    if not acumulado:
                        for b in batalha:
                            acumulado.append(b)
                    else:
                        for stat in por_batalha:
                            if stat["player"] not in [ac["player"] for ac in acumulado]:
                                acumulado.append(stat)
                            else:
                                for ac in acumulado:
                                    if ac["player"] == stat["player"]:
                                        ac["kp"] = ac["kp"] + stat["kp"]
                                        ac["dt"] = ac["dt"] + stat["dt"]
                    status = acumulado
            else:
                status = (
                    PlayerStatus.objects.filter(player__in=players_faixa_original)
                    .filter(data__gte=inicio)
                    .filter(data__lte=final)
                    .values(
                        "player",
                        "player__nick",
                        "player__game_id",
                        "player__alliance__tag",
                    )
                    .annotate(
                        kp=Max("killpoints") - Min("killpoints"),
                        dt=Max("deaths") - Min("deaths"),
                    )
                    .order_by(f"-{cat}")
                )

            media = 0
            contabilizar = 0

            for stat in status:
                player = Player.objects.get(pk=stat["player"])
                if player not in banidos_e_inativos and player not in farms:
                    abaterkp = 0
                    abaterdt = 0
                    abate_de_zeramento = 0

                    abate_mge = PontosDeMGE.objects.filter(kvk=kvk, player=player)
                    for pontos in abate_mge:
                        abaterkp = abaterkp + pontos.pontos
                        abaterdt = abaterdt + pontos.mortes

                    abate_de_zeramento = get_desconto_de_zeramento(
                        kvk_id=kvk.id, player_id=player.id
                    )
                    if abate_de_zeramento > 0:
                        abates_de_zerado[player.game_id] = abate_de_zeramento
                    if cat == "dt":
                        media = media + stat[cat] - abaterdt - abate_de_zeramento
                    else:
                        media = media + stat[cat] - abaterkp
                    contabilizar = contabilizar + 1

            if contabilizar:
                media = media // contabilizar

            adicionais = AdicionalDeFarms.objects.filter(kvk=kvk)
            adicionais_dic = {}
            for adicional in adicionais:
                adicionais_dic[adicional.player.game_id] = int(
                    adicional.t4_deaths * 0.25 + adicional.t5_deaths * 0.5
                )
            context["adicionais"] = adicionais_dic
            context["abates_de_zerados"] = abates_de_zerado

            mge_controlado = PontosDeMGE.objects.filter(kvk=kvk)
            abate_mge_dic = {}
            for pontos in mge_controlado:
                if pontos.player.game_id not in abate_mge_dic:
                    abate_mge_dic[pontos.player.game_id] = {
                        "kp": int(pontos.pontos),
                        "dt": int(pontos.mortes),
                    }
                else:
                    abate_mge_dic[pontos.player.game_id] = {
                        "kp": abate_mge_dic[pontos.player.game_id]["kp"]
                        + int(pontos.pontos),
                        "dt": abate_mge_dic[pontos.player.game_id]["dt"]
                        + int(pontos.mortes),
                    }
            context["abateMGE"] = abate_mge_dic

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

    return context


def analisedesempenho(request, kvkid, cat):
    kvk = Kvk.objects.get(pk=kvkid)

    if cat not in ["kp", "dt"]:
        return render(request, "rise/404.html")

    if kvk.id == 4:
        return render(request, "rise/404.html")

    consolidado = Consolidado.objects.filter(kvk=kvk)

    context = calcular(kvk, cat)

    cache.set(f"context_{cat}_{kvk.id}", context, 60 * 60)

    return render(request, "kvk/analise.html", context=context)


@login_required
def consolidar_kvk(request, kvkid):
    kvk = Kvk.objects.get(pk=kvkid)

    context = calcular(kvk, "dt")

    categorias = context["categorizados"]
    zerados = context["zerados"]

    for categoria in categorias:
        posicao = 1
        media = categoria["media"]
        meia_media = categoria["meiamedia"]
        for status in categoria["membros"]:
            player = Player.objects.get(game_id=status["player__game_id"])
            novo = Consolidado()
            novo.kvk = kvk
            novo.player = player
            novo.kp = status["kp"]
            novo.dt = status["dt"]
            novo.posicao_dt = posicao
            if player.pk in zerados:
                novo.cor_dt = "GRA"
                novo.zerado = True
            elif novo.dt >= media:
                novo.cor_dt = "GRE"
            elif novo.dt >= meia_media:
                novo.cor_dt = "YEL"
            else:
                novo.cor_dt = "RED"
            novo.save()
            posicao = posicao + 1

    return redirect("/")


@login_required
def adicionar_farms(request):
    if request.method == "POST":
        kvk = Kvk.objects.filter(id=request.POST["kvkid"]).first()
        player = Player.objects.filter(game_id=request.POST["player_id"]).first()

        if kvk and player:
            novo = AdicionalDeFarms()
            novo.t4_deaths = request.POST["t4"]
            novo.t5_deaths = request.POST["t5"]
            novo.player = player
            novo.kvk = kvk
            novo.save()
            logger.debug(
                "%s adicionou dados de farm para %s no %s",
                request.user.username,
                player.game_id,
                kvk,
            )
    return redirect(f"/kvk/analise/{request.POST['kvkid']}/{request.POST['cat']}/")


@login_required
def adicionar_mge_controlado(request):
    if request.method == "POST":
        kvk = Kvk.objects.filter(id=request.POST["kvkid"]).first()
        player = Player.objects.filter(game_id=request.POST["player_id"]).first()

        if kvk and player:
            novo = PontosDeMGE()
            novo.pontos = request.POST["pontos"]
            novo.mortes = request.POST["mortes"]
            novo.player = player
            novo.kvk = kvk
            novo.save()
            logger.debug(
                "%s adicionou pontos de MGE para %s no %s",
                request.user.username,
                player.game_id,
                kvk,
            )
    return redirect(f"/kvk/analise/{request.POST['kvkid']}/{request.POST['cat']}/")


def registrar_etapa(request, kvkid):
    if request.method == "POST":
        etapamanualform = EtapaForm(request.POST)
        if etapamanualform.is_valid():
            nova = Etapas()
            kvk_id = request.POST["kvk"]
            kvk = Kvk.objects.filter(pk=kvk_id).first()
            nova.kvk = kvk
            nova.date = request.POST["date"]
            nova.descricao = request.POST["descricao"]
            nova.save()
            return redirect(f"/kvk/edit/{kvkid}/")

    kvk = Kvk.objects.filter(pk=kvkid).first()
    etapamanualform = EtapaForm(initial={"kvk": kvk})

    etapas = Etapas.objects.filter(kvk=kvk)

    subirplanilhaform = UploadEtapasFileForm()

    context = {
        "form": etapamanualform,
        "subiretapasform": subirplanilhaform,
        "etapas": etapas,
        "kvk": kvk,
    }

    return render(request, "kvk/etapa.html", context=context)


@login_required
def etapas_por_planilha(request, kvkid):
    if request.method == "POST":
        form = UploadEtapasFileForm(request.POST, request.FILES)
        if form.is_valid():
            kvk = Kvk.objects.get(pk=kvkid)
            with open("etapas.csv", "wb") as destination:
                for chunk in request.FILES["file"].chunks():
                    destination.write(chunk)
            with open("./etapas.csv", encoding="utf-8") as etapas_file:
                reader = csv.reader(etapas_file)
                for row in reader:
                    # jump header
                    if row[0] == "Crônica":
                        continue
                    etapa = Etapas()
                    etapa.kvk = kvk
                    etapa.descricao = row[0]
                    etapa.date = timezone.make_aware(datetime.fromisoformat(row[1]))
                    etapa.save()

    return redirect(f"/kvk/etapa/{kvkid}/")


@login_required
def clear_etapas(request, kvkid):
    kvk = Kvk.objects.get(pk=kvkid)
    etapas_do_kvk = Etapas.objects.filter(kvk=kvk)

    for etapa in etapas_do_kvk:
        etapa.delete()

    return redirect(f"/kvk/etapa/{kvkid}/")


@login_required
def cargos_view(request, kvkid):
    if request.method == "POST":
        form = CargoForm(request.POST or None)

        if form.is_valid():
            form.save()
            logger.debug(
                "%s adicionou cargos no kvk %s", request.user.username, str(kvkid)
            )

    kvk = Kvk.objects.get(pk=kvkid)
    form = CargoForm(initial={"kvk": kvk})
    form.fields["player"].queryset = Player.objects.filter(alliance__in=[1, 2])

    cargos_neste_kvk = Cargo.objects.filter(kvk=kvk)

    context = {
        "kvk": kvk,
        "form": form,
        "cargos": cargos_neste_kvk,
    }

    return render(request, "kvk/cargo.html", context=context)


@login_required
def remove_cargo(request, cargoid):
    cargo = Cargo.objects.get(pk=cargoid)
    kvkid = cargo.kvk.id
    if cargo:
        cargo.delete()

    return redirect(f"/kvk/edit/{kvkid}/")


def get_desconto_de_zeramento(kvk_id, player_id):
    zeramentos = Zerado.objects.filter(kvk=kvk_id, player=player_id)

    if zeramentos:
        total_mortos = 0
        for zeramento in zeramentos:
            status_antes = (
                PlayerStatus.objects.filter(data__lte=zeramento.date, player=player_id)
                .order_by("-data")
                .first()
            )
            status_depois = (
                PlayerStatus.objects.filter(data__gte=zeramento.date, player=player_id)
                .order_by("data")
                .first()
            )

            mortos = status_depois.deaths - status_antes.deaths
            total_mortos = total_mortos + mortos

        return total_mortos

    return 0


@login_required
def config_kvk(request, kvkid):
    kvk = Kvk.objects.get(pk=kvkid)

    if request.method == "POST":
        form = KvkConfigForm(request.POST or None, instance=kvk)

        if form.is_valid():
            form.save()

    form = KvkConfigForm(
        initial={
            "inicio": kvk.inicio,
            "final": kvk.final,
            "primeira_luta": kvk.primeira_luta,
            "tipo": kvk.tipo,
        },
    )

    context = {
        "form": form,
        "kvk": kvk,
    }

    return render(request, "kvk/config.html", context=context)


def dkp_view(request, kvkid):
    kvk = Kvk.objects.get(pk=kvkid)

    context = {
        "kvk": kvk,
    }

    inicio = kvk.inicio
    if kvk.primeira_luta:
        inicio = kvk.primeira_luta

    final = kvk.final
    if not final:
        final = timezone.now()

    primeiro = (
        PlayerStatus.objects.filter(data__gte=kvk.inicio).order_by("data").first()
    )

    if not primeiro:
        return redirect(f"/kvk/edit/{kvk.id}/")

    status = (
        PlayerStatus.objects.exclude(player__status__in=["BANIDO", "INATIVO", "FARM"])
        .filter(
            data__year=primeiro.data.year,
            data__month=primeiro.data.month,
            data__day=primeiro.data.day,
        )
        .values(
            "player",
            "player__nick",
            "player__game_id",
            "player__alliance__tag",
            "power",
            "data",
            "killst4",
            "killst5",
        )
        .order_by("-data")
    )

    jafoi = []
    dkps = []
    for st in status:
        if st["player"] in jafoi:
            continue
        jafoi.append(st["player"])
        player = Player.objects.get(pk=st["player"])

        status_final = (
            PlayerStatus.objects.filter(
                data__gte=inicio, data__lte=final, player=st["player"]
            )
            .order_by("-data")
            .first()
        )

        if not status_final:
            logger.debug("Não foi possível calcular o DKP de: %s", st["player"])
            continue

        kvkstatus = KvKStatus.objects.filter(kvk=kvk, player=player).first()
        if not kvkstatus:
            kvkstatus = KvKStatus()

        poder = st["power"]
        coef = 0.2
        desconto_poder = 0
        if poder <= 50000000:
            desconto_poder = poder * coef
        elif poder > 50000000:
            desconto_poder = 50000000 * coef + (poder - 50000000) * 0.5

        # DKP=(T4kill*2)+(T5kill*4)+(T4death*5)+(T5death*10)+(Honra)+(PointsOnMaraunders)-(combatpower*20%)
        dkps.append(
            {
                "player": player.nick,
                "game_id": player.game_id,
                "dkp": int(
                    ((status_final.killst4 - st["killst4"]) * 0.4)
                    + ((status_final.killst5 - st["killst5"]) * 1)
                    + ((kvkstatus.deatht4) * 5)  # deaths t4
                    + ((kvkstatus.deatht5) * 10)  # deaths t5
                    # + (kvkstatus.honra)  # honra
                    # + (kvkstatus.marauders)  # pontos nos marauders
                    # - desconto_poder  # desconto de poder
                ),
                "killst4": status_final.killst4 - st["killst4"],
                "killst5": status_final.killst5 - st["killst5"],
                "deatht4": kvkstatus.deatht4,
                "deatht5": kvkstatus.deatht5,
                "desconto": desconto_poder,
            }
        )

    context["status"] = sorted(dkps, key=lambda k: k["dkp"], reverse=True)

    return render(request, "kvk/dkp.html", context=context)


@login_required
def status_dkp(request, kvkid, player):
    kvk = Kvk.objects.get(pk=kvkid)
    player = Player.objects.get(game_id=player)

    status, _ = KvKStatus.objects.get_or_create(kvk=kvk, player=player)

    form = KvKStatusForm(
        initial={
            "kvk": kvk,
            "player": player,
            "deatht4": status.deatht4,
            "deatht5": status.deatht5,
            "honra": status.honra,
            "marauders": status.marauders,
        }
    )
    if request.method == "POST":
        form = KvKStatusForm(request.POST or None)

        if form.is_valid():
            status.deatht4 = form.cleaned_data["deatht4"]
            status.deatht5 = form.cleaned_data["deatht5"]
            status.honra = form.cleaned_data["honra"]
            status.marauders = form.cleaned_data["marauders"]
            status.save()

    context = {
        "form": form,
        "kvk": kvk,
        "player": player,
    }

    return render(request, "kvk/status_dkp.html", context=context)


@login_required
def upload_hoh_csv(request, kvkid):
    """
    View responsável por processar o upload de um arquivo CSV contendo dados dos jogadores.

    Args:
        request (HttpRequest): O objeto HttpRequest contendo os dados da requisição.

    Returns:
        HttpResponse: O objeto HttpResponse redirecionando para a página de confirmação de população dos jogadores.

    """
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            with open("hoh.csv", "wb") as destination:
                for chunk in request.FILES["file"].chunks():
                    destination.write(chunk)
            with open("./hoh.csv", encoding="utf-8") as dados_csv:
                reader = csv.reader(dados_csv)
                for row in reader:
                    # jump header
                    if row[0] == "ID":
                        continue
                    player = Player.objects.filter(game_id=row[0]).first()
                    if player:
                        kvk = Kvk.objects.get(pk=kvkid)
                        status, _ = KvKStatus.objects.get_or_create(
                            kvk=kvk, player=player
                        )
                        status.deatht4 = int(row[6]) + int(row[7]) + int(row[8])
                        status.deatht5 = int(row[2]) + int(row[3]) + int(row[4])
                        status.save()
                    else:
                        logger.debug(
                            "Não foi possível criar KvKStatus para o ID: %s", row[0]
                        )
            return HttpResponseRedirect(f"/kvk/dkp/{kvkid}/")
    else:
        form = UploadFileForm()
    return render(request, "kvk/upload.html", {"form": form, "kvkid": kvkid})
