import csv
from datetime import datetime

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.db.models.aggregates import Max, Min
from django.utils import timezone

from players.models import Player, PlayerStatus

from kvk.forms import CargoForm, EtapaForm, UploadEtapasFileForm
from kvk.models import (
    Cargo,
    Etapas,
    Kvk,
    PontosDeMGE,
    Zerado,
    AdicionalDeFarms,
    faixas,
)

# Create your views here.


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

    return redirect("/kvk/")


def show_kvk(request, kvkid):
    kvk = Kvk.objects.filter(id=kvkid).first()

    zerados = Zerado.objects.filter(kvk=kvk)
    zerados_lista = []
    for zerado in zerados:
        zerados_lista.append(zerado.player)

    final = kvk.final
    if not final:
        final = timezone.now()

    farms_banidos_e_inativos = Player.objects.filter(
        status__in=["BANIDO", "FARM", "MIGROU", "INATIVO"]
    )

    topkp = (
        PlayerStatus.objects.all()
        .exclude(player__in=farms_banidos_e_inativos)
        .filter(data__gte=kvk.inicio)
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
        .filter(data__gte=kvk.inicio)
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
    kvk.save()
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
        return redirect(f"/kvk/edit/{running_kvk.id}/")

    return render(request, "rise/404.html")


@login_required
def removezerado(request, kvk, zerado_id):
    zerado = Zerado.objects.get(pk=zerado_id)
    if kvk == zerado.kvk.id:
        zerado.delete()

    return redirect(f"/kvk/edit/{zerado.kvk.id}/")


def analisedesempenho(request, kvkid, cat):
    kvk = Kvk.objects.get(pk=kvkid)

    if cat not in ["kp", "dt"]:
        return render(request, "rise/404.html")

    if kvk.id == 4:
        return render(request, "rise/404.html")

    final = kvk.final
    if not final:
        final = timezone.now()

    context = {
        "tipo": cat,
        "kvk": kvkid,
    }

    context = cache.get(f"context_{cat}_{kvk.id}") or context

    if "zerados" not in context:
        banidos_e_inativos = Player.objects.filter(
            status__in=["BANIDO", "INATIVO"]
        )
        banidos_inativos_ids = []
        for player in banidos_e_inativos:
            banidos_inativos_ids.append(player.id)

        primeiro = (
            PlayerStatus.objects.filter(data__gte=kvk.inicio)
            .order_by("data")
            .first()
        )

        if not primeiro:
            return redirect(f"/kvk/edit/{kvk.id}/")

        zerados = Zerado.objects.filter(kvk=kvk)
        zerados_lista = []
        zerados_ids = []
        for zerado_pra_lista in zerados:
            zerados_lista.append(zerado_pra_lista.player)
            zerados_ids.append(zerado_pra_lista.player.id)

        context["zerados"] = zerados_ids
        context["banidos_inativos"] = banidos_inativos_ids

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

            status = (
                PlayerStatus.objects.filter(player__in=players_faixa_original)
                .filter(data__gte=kvk.inicio)
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
                if (
                    not player in zerados_lista
                    and not player in banidos_e_inativos
                ):
                    abater = 0
                    if cat == "kp":
                        abate_mge = PontosDeMGE.objects.filter(
                            kvk=kvk, player=player
                        )
                        for pontos in abate_mge:
                            abater = abater + pontos.pontos
                    media = media + stat[cat] - abater
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

            mge_controlado = PontosDeMGE.objects.filter(kvk=kvk)
            abate_mge_dic = {}
            for pontos in mge_controlado:
                if pontos.player.game_id not in abate_mge_dic:
                    abate_mge_dic[pontos.player.game_id] = int(pontos.pontos)
                else:
                    abate_mge_dic[pontos.player.game_id] = abate_mge_dic[
                        pontos.player.game_id
                    ] + int(pontos.pontos)
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
            cache.set(f"context_{cat}_{kvk.id}", context, 60 * 60)

    return render(request, "kvk/analise.html", context=context)


@login_required
def adicionar_farms(request):
    if request.method == "POST":
        kvk = Kvk.objects.filter(id=request.POST["kvkid"]).first()
        print(kvk)
        player = Player.objects.filter(
            game_id=request.POST["player_id"]
        ).first()

        if kvk and player:
            novo = AdicionalDeFarms()
            novo.t4_deaths = request.POST["t4"]
            novo.t5_deaths = request.POST["t5"]
            novo.player = player
            novo.kvk = kvk
            novo.save()
    return redirect(
        f"/kvk/analise/{request.POST['kvkid']}/{request.POST['cat']}/"
    )


@login_required
def adicionar_mge_controlado(request):
    if request.method == "POST":
        kvk = Kvk.objects.filter(id=request.POST["kvkid"]).first()
        print(kvk)
        player = Player.objects.filter(
            game_id=request.POST["player_id"]
        ).first()

        if kvk and player:
            novo = PontosDeMGE()
            novo.pontos = request.POST["pontos"]
            novo.player = player
            novo.kvk = kvk
            novo.save()
    return redirect(
        f"/kvk/analise/{request.POST['kvkid']}/{request.POST['cat']}/"
    )


def registrar_etapa(request, kvkid):
    if request.method == "POST":
        etapamanualform = EtapaForm(request.POST)
        print(request.POST["kvk"])
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
                    etapa.date = timezone.make_aware(
                        datetime.fromisoformat(row[1])
                    )
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
