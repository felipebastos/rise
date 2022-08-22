import csv
from datetime import datetime

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Max, Min
from django.utils import timezone
from kvk.forms import EtapaForm, UploadEtapasFileForm

from players.models import Player, PlayerStatus

from .models import Etapas, Kvk, Zerado, AdicionalDeFarms

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

    farms_banidos_e_inativos = Player.objects.filter(status__in=['BANIDO', 'FARM', 'MIGROU', 'INATIVO'])

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

    return render(request, 'rise/404.html')


@login_required
def removezerado(request, kvk, zerado_id):
    zerado = Zerado.objects.get(pk=zerado_id)
    zerado.delete()

    return redirect(f"/kvk/edit/{zerado.kvk.id}/")


def analisedesempenho(request, kvkid, cat):
    kvk = Kvk.objects.get(pk=kvkid)

    if cat not in ["kp", "dt"]:
        return render(request, 'rise/404.html')

    if kvk.id == 4:
        return render(request, 'rise/404.html')

    final = kvk.final
    if not final:
        final = timezone.now()

    context = {
        "tipo": cat,
    }

    banidos_e_inativos = Player.objects.filter(status__in=['BANIDO', 'INATIVO'])

    faixas = [
        (100000001, 5000000000, 3000000),
        (90000001, 100000000, 2200000),
        (80000001, 90000000, 1500000),
        (70000001, 80000000, 1100000),
        (60000001, 70000000, 700000),
        (50000001, 60000000, 600000),
        (40000001, 50000000, 500000),
        (0, 40000000, 500000),
    ]

    primeiro = (
        PlayerStatus.objects.filter(data__gte=kvk.inicio)
        .order_by("data")
        .first()
    )

    if not primeiro:
        return redirect(f"/kvk/edit/{kvk.id}/")

    categorizados = []
    for faixa in faixas:
        zerados = Zerado.objects.filter(kvk=kvk)
        zerados_lista = []
        for zerado_pra_lista in zerados:
            zerados_lista.append(zerado_pra_lista.player)

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
                if (
                    stat.data.hour == primeiro.data.hour
                ):
                    players_faixa_original.append(stat.player)

        status = (
            PlayerStatus.objects
            .filter(player__in=players_faixa_original)
            .filter(data__gte=kvk.inicio)
            .filter(data__lte=final)
            .values("player", "player__nick", "player__game_id", "player__alliance__tag")
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
            if not player in zerados_lista and not player in banidos_e_inativos:
                media = media + stat[cat]
                contabilizar = contabilizar + 1

        media = media // contabilizar

        adicionais = AdicionalDeFarms.objects.filter(kvk=kvk)
        adicionais_dic = {}
        for adicional in adicionais:
            adicionais_dic[adicional.player.game_id] = int(adicional.t4_deaths*0.25 + adicional.t5_deaths*0.5)
        context["adicionais"] = adicionais_dic

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
        context["kvk"] = kvkid

    return render(request, "kvk/analise.html", context=context)


@login_required
def adicionarFarms(request):
    print('Cheguei na adicionar.')
    if request.method == 'POST':
        for k in request.POST:
            print(f'{k}: {request.POST[k]}')
        kvk = Kvk.objects.filter(id=request.POST['kvkid']).first()
        print(kvk)
        player = Player.objects.filter(game_id=request.POST['player_id']).first()

        if kvk and player:
            novo = AdicionalDeFarms()
            novo.t4_deaths = request.POST['t4']
            novo.t5_deaths = request.POST['t5']
            novo.player = player
            novo.kvk = kvk
            novo.save()
    return redirect(f"/kvk/analise/{request.POST['kvkid']}/{request.POST['cat']}/")


def registrarEtapa(request, kvkid):
    if request.method == 'POST':
        etapamanualform = EtapaForm(request.POST)
        print(request.POST['kvk'])
        if etapamanualform.is_valid():
            nova = Etapas()
            id = request.POST['kvk']
            kvk = Kvk.objects.filter(pk=id).first()
            nova.kvk = kvk
            nova.date = request.POST['date']
            nova.descricao = request.POST['descricao']
            nova.save()
            return redirect(f'/kvk/edit/{kvkid}/')

    kvk = Kvk.objects.filter(pk=kvkid).first()
    etapamanualform = EtapaForm(initial={'kvk': kvk})

    etapas = Etapas.objects.filter(kvk=kvk)

    subirplanilhaform = UploadEtapasFileForm()

    context = {
        'form': etapamanualform,
        'subiretapasform': subirplanilhaform,
        'etapas': etapas,
        'kvk': kvk,
    }

    return render(request, 'kvk/etapa.html', context=context)


@login_required
def etapas_por_planilha(request, kvkid):
    if request.method == "POST":
        form = UploadEtapasFileForm(request.POST, request.FILES)
        if form.is_valid():
            kvk = Kvk.objects.get(pk=kvkid)
            with open("etapas.csv", "wb") as destination:
                for chunk in request.FILES["file"].chunks():
                    destination.write(chunk)
            with open("./etapas.csv", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                # jump header
                    if row[0] == "Crônica":
                        continue
                    etapa = Etapas()
                    etapa.kvk = kvk
                    etapa.descricao = row[0]
                    etapa.date = timezone.make_aware(datetime.fromisoformat(row[1]))
                    etapa.save()

    return redirect(f'/kvk/etapa/{kvkid}/')


@login_required
def clear_etapas(request, kvkid):
    kvk = Kvk.objects.get(pk=kvkid)
    etapas_do_kvk = Etapas.objects.filter(kvk=kvk)

    for etapa in etapas_do_kvk:
        etapa.delete()

    return redirect(f'/kvk/etapa/{kvkid}/')
