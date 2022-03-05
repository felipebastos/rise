import csv

from django.shortcuts import redirect, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models.aggregates import Max, Min

from datetime import date

from .models import (
    Player,
    PlayerStatus,
    Alliance,
    player_status,
    player_rank,
    player_spec,
)
from .forms import UploadFileForm
from rise.forms import SearchPlayerForm
from kvk.models import Kvk, Zerado

# Create your views here.


def index(request, game_id):
    try:
        player = Player.objects.get(game_id=game_id)
        status = PlayerStatus.objects.filter(player__game_id=game_id).order_by(
            "-data"
        )
        spec = None
        for i, (res, verbose) in enumerate(player_spec):
            if player.specialty == res:
                spec = verbose
        temKvk = Kvk.objects.order_by("-inicio").first()
        exibirkvk = False
        if temKvk and temKvk.ativo:
            exibirkvk = True
        context = {
            "player": player,
            "status": status,
            "spec": spec,
            "showkvk": exibirkvk,
        }
    except Player.DoesNotExist:
        raise Http404("Player não encontrado.")
    return render(request, "players/player.html", context)


@login_required
def edit_player(request, game_id):
    player = Player.objects.filter(game_id=game_id).first()

    if not player:
        raise Http404("Player não existe.")

    allies = Alliance.objects.all()

    if request.method == "GET":
        context = {
            "player": player,
            "status_list": player_status,
            "ranks_list": player_rank,
            "specialty_list": player_spec,
            "alliances": allies,
        }
        return render(request, "players/edit.html", context=context)
    player.nick = request.POST["nick"]
    player.observacao = request.POST["observacao"]
    player.status = request.POST["status"]
    player.rank = request.POST["rank"]
    player.specialty = request.POST["specialty"]
    player.alliance = Alliance.objects.filter(tag=request.POST["ally"]).first()
    player.alterado_por = request.user
    player.save()
    context = {
        "player": player,
        "status_list": player_status,
        "ranks_list": player_rank,
        "specialty_list": player_spec,
        "alliances": allies,
    }
    return render(request, "players/edit.html", context=context)


@login_required
def listspecs(request, spec):
    players = Player.objects.filter(specialty=spec).order_by("alliance")

    specialty = None
    for i, (code, verbose) in enumerate(player_spec):
        if code == spec:
            specialty = verbose

    context = {
        "players": players,
        "spec": specialty,
        "total": len(players),
    }

    return render(request, "players/spec.html", context=context)


@login_required
def review_players(request, ally_tag):
    if request.method == "GET":
        try:
            ally = Alliance.objects.filter(tag=ally_tag).first()

            if ally:
                membros = Player.objects.filter(alliance=ally)

                context = {
                    "membros": membros,
                    "ally": ally,
                    "total": len(membros),
                }
                return render(request, "players/review.html", context)
        except:
            raise Http404("Aliança não está nos registros.")
    else:
        membros = Player.objects.filter(alliance__tag=ally_tag)
        semalianca = Alliance.objects.filter(tag="PSA").first()
        for membro in membros:
            if membro.game_id in request.POST:
                membro.alliance = semalianca
                membro.alterado_por = request.user
                membro.alterado_em = date.today()
                membro.save()
        return redirect(f"/players/review/{ally_tag}/")


def findplayer(request):
    if request.method == "POST":
        form = SearchPlayerForm(request.POST)
        if form.is_valid():
            id = request.POST["id"]
            return redirect(f"/players/{id}")
        else:
            raise Http404("Você não procurou por dados válidos.")
    else:
        raise Http404("Só sirvo para buscas do formulário.")


@login_required
def add_status(request, game_id):
    try:
        poder = ""
        if "." in request.POST["poder"]:
            poder = request.POST["poder"].replace(".", "")
        else:
            poder = request.POST["poder"]
        kp = ""
        if "." in request.POST["killpoints"]:
            kp = request.POST["killpoints"].replace(".", "")
        else:
            kp = request.POST["killpoints"]
        deaths = ""
        if "." in request.POST["mortes"]:
            deaths = request.POST["mortes"].replace(".", "")
        else:
            deaths = request.POST["mortes"]
        player = Player.objects.filter(game_id=game_id).first()

        novo_status = PlayerStatus()
        novo_status.player = player
        novo_status.power = poder
        novo_status.killpoints = kp
        novo_status.deaths = deaths
        novo_status.save()

        kvk = Kvk.objects.order_by("-inicio").first()
        # print(kvk)
        if kvk and kvk.ativo:
            honra = request.POST["honra"]
            zerado = 0
            try:
                if request.POST["zerado"]:
                    zerado = 1
            except:
                zerado = 0
            # print(zerado)
            return redirect(f"/kvk/update/{kvk.id}/{game_id}/{honra}/{zerado}/")
        if "origem" in request.POST:
            return redirect(request.POST["origem"])
        return redirect(f"/players/{game_id}/")
    except Exception as e:
        raise Http404("Player não existe.")


@login_required
def upload_csv(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            with open("dados.csv", "wb") as destination:
                for chunk in request.FILES["file"].chunks():
                    destination.write(chunk)
            return HttpResponseRedirect("/players/populate/")
    else:
        form = UploadFileForm()
    return render(request, "players/upload.html", {"form": form})


@login_required
def populate(request):
    with open("./dados.csv") as f:
        reader = csv.reader(f)
        for row in reader:
            # jump header
            if row[0] == "Governor ID":
                continue

            jogador = Player.objects.filter(game_id=row[0]).first()

            if jogador is None:
                # create new player
                jogador = Player()
                jogador.game_id = row[0]
                jogador.nick = row[2]
                psa = Alliance.objects.filter(tag="PSA").first()
                jogador.alliance = psa
                jogador.save()
            else:
                # update some data
                oldnick = jogador.nick
                print(f"Mudança de nick: {oldnick} > {row[2]}")
                jogador.nick = row[2]
                if jogador.nick != oldnick:
                    if jogador.observacao:
                        jogador.observacao += (
                            f"\r\nMudança de nick: {oldnick} > {row[2]}"
                        )
                    else:
                        jogador.observacao = (
                            f"Mudança de nick: {oldnick} > {row[2]}"
                        )
                ally = Alliance.objects.filter(tag=row[4]).first()
                if ally is not None:
                    jogador.alliance = ally
                else:
                    psa = Alliance.objects.filter(tag="PSA").first()
                    jogador.alliance = psa
                jogador.save()

            poder = row[3]
            if row[3] == "":
                poder = 0

            # Colunas de 5 a 9
            kills = []
            kills_t1 = row[5]
            if row[5] == "":
                kill_t1 = 0
            kills.append(kills_t1)
            kills_t2 = row[6]
            if row[6] == "":
                kill_t2 = 0
            kills.append(kills_t2)
            kills_t3 = row[7]
            if row[7] == "":
                kill_t3 = 0
            kills.append(kills_t3)
            kills_t4 = row[8]
            if row[8] == "":
                kill_t4 = 0
            kills.append(kills_t4)
            kills_t5 = row[9]
            if row[9] == "":
                kills_t5 = 0
            kills.append(kills_t5)

            killpoints = 0
            coeficientes = [0.2, 2, 5, 10, 20]
            for i in range(len(kills)):
                if isinstance(kills[i], str):
                    if "." in kills[i]:
                        kills[i] = kills[i].replace(".", "")
                    kills[i] = int(kills[i])

                killpoints = killpoints + kills[i] * coeficientes[i]

            death = row[10]
            if row[4] == "":
                death = 0

            statusnovo = PlayerStatus()
            statusnovo.player = jogador
            statusnovo.power = poder.replace(".", "")
            statusnovo.killpoints = killpoints
            statusnovo.deaths = death.replace(".", "")
            statusnovo.save()

    return HttpResponseRedirect("/")


@login_required
def alliance(request, ally_tag):
    try:
        ally = Alliance.objects.filter(tag=ally_tag).first()

        if ally:
            membros = Player.objects.filter(alliance=ally)

            paginator = Paginator(membros, 25)

            page_number = request.GET.get("page")

            pagina = paginator.get_page(page_number)

            kills = 0
            deaths = 0
            power = 0
            for membro in membros:
                status = (
                    PlayerStatus.objects.filter(player=membro)
                    .order_by("-data")
                    .first()
                )
                if status:
                    kills = kills + status.killpoints
                    deaths = deaths + status.deaths
                    power = power + status.power
            context = {
                "membros": pagina,
                "ally": ally,
                "total": len(membros),
                "kills": kills,
                "power": power,
                "death": deaths,
                "range": range(1, pagina.paginator.num_pages + 1),
            }
            return render(request, "players/alianca.html", context)
    except Exception as e:
        print(e)
        raise Http404("Aliança não está nos registros.")


@login_required
def top300(request):
    # jogadores = PlayerStatus.objects.all().exclude(player__alliance__tag='MIGR').order_by('-power')[:300]
    jogadores = []
    noreino = Player.objects.exclude(alliance__tag="MIGR")
    for jogador in noreino:
        status = (
            PlayerStatus.objects.filter(player=jogador)
            .order_by("-data")
            .first()
        )
        jogadores.append(status)
    jogadores.sort(
        key=lambda x: x.power if (x is not None) else 0, reverse=True
    )
    poderTotal = 0
    for jogador in jogadores[:300]:
        poderTotal = poderTotal + jogador.power
    context = {
        "jogadores": jogadores[:300],
        "poder": poderTotal,
    }
    return render(request, "players/top300.html", context=context)


@login_required
def falta_status(request, ally_tag):
    status = PlayerStatus.objects.all()
    id_quem_tem = []
    for cada in status:
        if cada.power != 0:
            id_quem_tem.append(cada.player.id)
    ally = Alliance.objects.filter(tag=ally_tag).first()
    jogadores_sem_status = Player.objects.filter(alliance=ally).exclude(
        id__in=id_quem_tem
    )

    context = {
        "players": jogadores_sem_status,
    }

    return render(request, "players/semstatus.html", context=context)


@login_required
def antigos(request, ally_tag):
    status = PlayerStatus.objects.all()
    hoje = timezone.now()
    id_quem_tem = []
    for cada in status:
        diff = hoje - cada.data
        if diff.days < 15:
            id_quem_tem.append(cada.player.id)
    ally = Alliance.objects.filter(tag=ally_tag).first()
    jogadores_sem_status = Player.objects.filter(alliance=ally).exclude(
        id__in=id_quem_tem
    )

    context = {
        "players": jogadores_sem_status,
    }

    return render(request, "players/antigos.html", context=context)


@login_required
def editaStatus(request, status_id):
    if request.method == "POST":
        status = PlayerStatus.objects.all().filter(id=status_id).first()
        if status.editavel():
            status.power = request.POST["power"]
            status.killpoints = request.POST["killpoints"]
            status.deaths = request.POST["deaths"]
            status.data = timezone.now()
            status.save()

        return redirect(f"/players/{status.player.game_id}")

    status = PlayerStatus.objects.all().filter(id=status_id).first()
    context = {"status": status}
    return render(request, "players/editastatus.html", context=context)


@login_required
def delete_status(request, status_id):
    status = PlayerStatus.objects.all().filter(id=status_id).first()
    if status.editavel():
        status.delete()

    return redirect(f"/players/{status.player.game_id}")


def como_estou(request):
    if request.method == "POST":
        kvk = Kvk.objects.filter(ativo=True).first()
        if not kvk:
            kvk = Kvk.objects.all().order_by("-inicio").first()

        id = request.POST["game_id"]
        o_player = Player.objects.filter(game_id=id).first()
        status = (
            PlayerStatus.objects.filter(player=o_player)
            .filter(data__gte=kvk.inicio)
            .order_by("data")
        )

        zerado = False
        if Zerado.objects.filter(kvk=kvk, player=o_player).first():
            zerado = True

        zerados = Zerado.objects.filter(kvk=kvk)
        zerados_lista = []
        for zerado_pra_lista in zerados:
            zerados_lista.append(zerado_pra_lista.player)

        primeiro = status.first()
        ultimo = status.last()

        status_kp = (
            PlayerStatus.objects.filter(data__gte=kvk.inicio)
            .values("player__nick")
            .annotate(
                kp=Max("killpoints") - Min("killpoints"),
                dt=Max("deaths") - Min("deaths"),
            )
            .order_by("-kp")
        )
        pos_kp = 1
        for stat in status_kp:
            if stat["player__nick"] != ultimo.player.nick:
                pos_kp = pos_kp + 1
            else:
                break

        status_dt = (
            PlayerStatus.objects.exclude(player__in=zerados_lista)
            .filter(data__gte=kvk.inicio)
            .values("player__nick")
            .annotate(
                kp=Max("killpoints") - Min("killpoints"),
                dt=Max("deaths") - Min("deaths"),
            )
            .order_by("-dt")
        )
        pos_dt = 1
        for stat in status_dt:
            if stat["player__nick"] != ultimo.player.nick:
                pos_dt = pos_dt + 1
            else:
                break
        faixa_inicio = 0
        faixa_fim = 10000000000
        meta = 0
        if primeiro.power > 100000000:
            faixa_inicio = 100000000
            meta = 3000000
        elif 90000000 < primeiro.power < 100000000:
            faixa_inicio = 90000000
            faixa_fim = 100000000
            meta = 2200000
        elif 80000000 < primeiro.power < 90000000:
            faixa_inicio = 80000000
            faixa_fim = 90000000
            meta = 1500000
        elif 70000000 < primeiro.power < 80000000:
            faixa_inicio = 70000000
            faixa_fim = 80000000
            meta = 1100000
        elif 60000000 < primeiro.power < 70000000:
            faixa_inicio = 60000000
            faixa_fim = 70000000
            meta = 700000
        elif 50000000 < primeiro.power < 60000000:
            faixa_inicio = 50000000
            faixa_fim = 60000000
            meta = 600000
        elif 40000000 < primeiro.power < 50000000:
            faixa_inicio = 40000000
            faixa_fim = 50000000
            meta = 500000
        else:
            faixa_inicio = 0
            faixa_fim = 40000000
            meta = 500000

        faixa_original = PlayerStatus.objects.filter(
            data__year=primeiro.data.year,
            data__month=primeiro.data.month,
            data__day=primeiro.data.day,
            power__gte=faixa_inicio,
            power__lte=faixa_fim,
        ).order_by("data")
        players_faixa_original = []
        for stat in faixa_original:
            if stat.player not in players_faixa_original:
                if (
                    stat.data.hour == primeiro.data.hour
                    and stat.data.minute == primeiro.data.minute
                ):
                    players_faixa_original.append(stat.player)

        status_kp_similares = (
            PlayerStatus.objects.all()
            .filter(player__in=players_faixa_original)
            .filter(data__gte=kvk.inicio)
            .values("player__nick")
            .annotate(
                kp=Max("killpoints") - Min("killpoints"),
                dt=Max("deaths") - Min("deaths"),
            )
            .order_by("-kp")
        )
        status_dt_similares = (
            PlayerStatus.objects.all()
            .filter(player__in=players_faixa_original)
            .filter(data__gte=kvk.inicio)
            .values("player__nick")
            .annotate(
                kp=Max("killpoints") - Min("killpoints"),
                dt=Max("deaths") - Min("deaths"),
            )
            .order_by("-dt")
        )

        todos_kp = len(status_kp_similares)
        pos_kp_faixa = todos_kp
        for stat in status_kp_similares:
            if stat["player__nick"] != ultimo.player.nick:
                pos_kp_faixa = pos_kp_faixa - 1
            else:
                break

        todos_dt = len(status_dt_similares)
        pos_dt_faixa = todos_dt
        for stat in status_dt_similares:
            if stat["player__nick"] != ultimo.player.nick:
                pos_dt_faixa = pos_dt_faixa - 1
            else:
                break

        context = {
            "kvk": kvk,
            "nick": ultimo.player.nick,
            "player_id": ultimo.player.game_id,
            "primeirostatus": primeiro,
            "atualizado": ultimo.data,
            "killpoints": ultimo.killpoints - primeiro.killpoints,
            "deaths": ultimo.deaths - primeiro.deaths,
            "power": (ultimo.power - primeiro.power) * -1,
            "perdeuganhou": "Ganhou"
            if ultimo.power > primeiro.power
            else "Perdeu",
            "poskp": pos_kp,
            "posdt": pos_dt,
            "todoskp": todos_kp,
            "poskpfaixa": pos_kp_faixa,
            "todosdt": todos_dt,
            "posdtfaixa": pos_dt_faixa,
            "comparadoa": players_faixa_original,
            "metamortes": True
            if meta < ultimo.deaths - primeiro.deaths
            else False,
            "meta": meta,
            "zerado": zerado,
        }

        return render(request, "players/emkvk.html", context=context)
    else:
        return Http404(request)
