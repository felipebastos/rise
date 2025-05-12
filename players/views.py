import csv
import logging
from datetime import date

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.aggregates import Max, Min
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils import timezone

from bank.models import Credito
from kvk.models import (
    Cargo,
    Consolidado,
    Etapas,
    Kvk,
    PontosDeMGE,
    Zerado,
    get_minha_faixa,
)
from mge.models import EventoDePoder, Mge, Punido
from players.forms import AddFarmForm, UploadFileForm
from players.models import (
    CARGO,
    PLAYER_STATUS,
    Advertencia,
    Alliance,
    Player,
    PlayerStatus,
    player_rank,
    player_spec,
)
from rise.forms import SearchPlayerForm
from utils.datas import get_datas

# Create your views here.
logger = logging.getLogger("k32")


def index(request, game_id):
    """
    View responsável por exibir a página de perfil de um jogador.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém os
                                             detalhes da requisição HTTP.

        game_id (int): O ID do jogo do jogador.

    Returns:
        HttpResponse: O objeto HttpResponse que contém a
                                 resposta HTTP com a página renderizada.

    Raises:
        Player.DoesNotExist: Se o jogador com o ID do jogo especificado não existir.

    """
    try:
        player = Player.objects.get(game_id=game_id)
        status = PlayerStatus.objects.filter(player__game_id=game_id).order_by("-data")

        grafico = PlayerStatus.objects.filter(player__game_id=game_id)

        spec = None
        for _, (res, verbose) in enumerate(player_spec):
            if player.specialty == res:
                spec = verbose
        tem_kvk = Kvk.objects.order_by("-inicio").first()
        exibirkvk = False
        if tem_kvk and tem_kvk.ativo:
            exibirkvk = True

        punido = Punido.objects.filter(player=player)
        punido_poder = EventoDePoder.objects.filter(player=player)
        advertencias_do_player = Advertencia.objects.filter(player=player)

        etapas = Etapas.objects.all()

        elementos = []
        for etapa in etapas:
            elementos.append(etapa)
        for stat in status:
            elementos.append(stat)

        def order_by_date(evento):
            if isinstance(evento, Etapas):
                return evento.date
            return evento.data

        elementos.sort(reverse=True, key=order_by_date)

        cargos = Cargo.objects.filter(player=player)

        kvks = Consolidado.objects.filter(player=player).order_by("-kvk__inicio")

        farm_form = AddFarmForm()

        context = {
            "player": player,
            "status": status,
            "spec": spec,
            "showkvk": exibirkvk,
            "punicoesMge": punido,
            "punicoesPoder": punido_poder,
            "advertencias": advertencias_do_player,
            "elementos": elementos,
            "cargos": cargos,
            "farmform": farm_form,
            "grafico": grafico,
            "kvks": kvks,
        }
    except Player.DoesNotExist:
        return render(request, "rise/404.html")
    return render(request, "players/player.html", context)


@login_required
def edit_player(request, game_id):
    """
    View responsável por editar um jogador.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém os dados da requisição.
        game_id (int): O ID do jogo do jogador a ser editado.

    Returns:
        HttpResponse: O objeto HttpResponse que representa a resposta da requisição.

    Raises:
        None
    """
    player = Player.objects.filter(game_id=game_id).first()

    if not player:
        return render(request, "rise/404.html")

    allies = Alliance.objects.all()

    if request.method == "GET":
        context = {
            "player": player,
            "status_list": PLAYER_STATUS,
            "ranks_list": player_rank,
            "specialty_list": player_spec,
            "func_list": CARGO,
            "alliances": allies,
        }
        return render(request, "players/edit.html", context=context)
    player.nick = request.POST["nick"]
    player.observacao = request.POST["observacao"]
    player.status = request.POST["status"]
    player.rank = request.POST["rank"]
    player.specialty = request.POST["specialty"]
    player.func = request.POST["func"]
    player.alliance = Alliance.objects.filter(tag=request.POST["ally"]).first()
    player.alterado_por = request.user
    player.alterado_em = timezone.now()
    player.save()
    logger.debug("%s editou %s", request.user.username, player.game_id)
    context = {
        "player": player,
        "status_list": PLAYER_STATUS,
        "ranks_list": player_rank,
        "specialty_list": player_spec,
        "func_list": CARGO,
        "alliances": allies,
    }
    return render(request, "players/edit.html", context=context)


@login_required
def listspecs(request, spec):
    """
    View que lista os jogadores de uma especialidade específica.

    Args:
        request (HttpRequest): O objeto HttpRequest que representa a requisição HTTP.
        spec (str): A especialidade dos jogadores a serem listados.

    Returns:
        HttpResponse: O objeto HttpResponse que representa a
                                resposta HTTP contendo a página renderizada
                                com a lista de jogadores.

    Raises:
        Nenhum.

    """
    players = Player.objects.filter(specialty=spec).order_by("alliance")

    specialty = None
    for _, (code, verbose) in enumerate(player_spec):
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
    """
    View que exibe e permite a revisão dos jogadores de uma aliança.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém os dados da requisição.
        ally_tag (str): A tag da aliança.

    Returns:
        HttpResponse: O objeto HttpResponse que contém a resposta da view.

    Raises:
        None
    """
    if request.method == "GET":
        ally = Alliance.objects.filter(tag=ally_tag).first()

        if ally:
            membros = Player.objects.filter(alliance=ally)

            context = {
                "membros": membros,
                "ally": ally,
                "total": len(membros),
            }
            return render(request, "players/review.html", context)

        return render(request, "rise/404.html")

    membros = Player.objects.filter(alliance__tag=ally_tag)
    semalianca = Alliance.objects.filter(tag="PSA").first()
    for membro in membros:
        if membro.game_id in request.POST:
            membro.alliance = semalianca
            membro.alterado_por = request.user
            membro.alterado_em = date.today()
            membro.save()
            logger.debug("%s editou %s", request.user.username, membro.game_id)
    return redirect(f"/players/review/{ally_tag}/")


def findplayer(request):
    """
    View responsável por buscar um jogador no sistema.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém os dados da requisição.

    Returns:
        HttpResponse: O objeto HttpResponse que representa a resposta da view.

    Raises:
        None

    """
    if request.method == "POST":
        form = SearchPlayerForm(request.POST)
        if form.is_valid():
            busca = request.POST["busca"]
            player = Player.objects.filter(game_id=busca).first()
            if not player:
                if request.user.is_authenticated:
                    players = Player.objects.filter(
                        Q(nick__icontains=busca) | Q(observacao__icontains=busca)
                    )
                else:
                    players = Player.objects.filter(nick__icontains=busca)
                context = {
                    "membros": players,
                    "termo": busca,
                }
                return render(request, "players/searchresult.html", context=context)
            return redirect(f"/players/{player.game_id}/")
        return render(request, "rise/404.html")
    return render(request, "rise/404.html")


@login_required
def add_status(request, game_id):
    """
    View responsável por adicionar um novo status de jogador.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém os dados da requisição.
        game_id (int): O ID do jogo ao qual o jogador pertence.

    Returns:
        HttpResponse: O objeto HttpResponse que representa a resposta da view.

    Raises:
        KeyError: Se alguma chave não existir no dicionário request.POST.

    """
    try:
        poder = ""
        if "." in request.POST["poder"]:
            poder = request.POST["poder"].replace(".", "")
        else:
            poder = request.POST["poder"]
        killpoints = ""
        if "." in request.POST["killpoints"]:
            killpoints = request.POST["killpoints"].replace(".", "")
        else:
            killpoints = request.POST["killpoints"]
        deaths = ""
        if "." in request.POST["mortes"]:
            deaths = request.POST["mortes"].replace(".", "")
        else:
            deaths = request.POST["mortes"]
        player = Player.objects.filter(game_id=game_id).first()

        novo_status = PlayerStatus()
        novo_status.player = player
        novo_status.power = poder
        novo_status.killpoints = killpoints
        novo_status.deaths = deaths
        novo_status.save()
        logger.debug(
            "%s adicionou status %s", request.user.username, novo_status.player.game_id
        )

        kvk = Kvk.objects.order_by("-inicio").first()

        if kvk and kvk.ativo:
            honra = request.POST["honra"]
            zerado = 0

            if "zerado" in request.POST:
                zerado = 1

            return redirect(f"/kvk/update/{kvk.id}/{game_id}/{honra}/{zerado}/")
        if "origem" in request.POST:
            return redirect(request.POST["origem"])
        return redirect(f"/players/{game_id}/")
    except KeyError as exception:
        context = {
            "exception": exception,
        }
        return render(request, "rise/404.html", context=context)


@login_required
def upload_csv(request):
    """
    View responsável por processar o upload de um arquivo
    CSV contendo dados dos jogadores.

    Args:
        request (HttpRequest): O objeto HttpRequest contendo os dados da requisição.

    Returns:
        HttpResponse: O objeto HttpResponse redirecionando para a página de
                                confirmação de população dos jogadores.

    """
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            cache.set("upload_date", form.cleaned_data["dia"], 20)
            with open("dados.csv", "wb") as destination:
                for chunk in request.FILES["file"].chunks():
                    destination.write(chunk)
            return HttpResponseRedirect("/players/confirm/populate/")
    else:
        form = UploadFileForm()
    return render(request, "players/upload.html", {"form": form})


@login_required
def confirm_populate(request):
    """
    View que popula a comparação de jogadores a partir de um arquivo CSV.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém os dados da requisição.

    Returns:
        HttpResponse: O objeto HttpResponse que representa a resposta da view.

    Raises:
        Nenhum.

    """
    comparison = []
    with open("./dados.csv", encoding="utf-8") as dados_csv:
        reader = csv.reader(dados_csv)
        for row in reader:
            if row[0] == "Governor ID":
                continue
            jogador = Player.objects.filter(game_id=row[0]).first()
            if jogador:
                comparison.append(
                    {
                        "tipo": "atualização",
                        "original": jogador,
                        "novo": {
                            "game_id": row[0],
                            "nick": row[2],
                            "ally": row[4],
                        },
                    }
                )
            else:
                comparison.append(
                    {
                        "tipo": "adição",
                        "novo": {
                            "game_id": row[0],
                            "nick": row[2],
                            "ally": row[4],
                        },
                    }
                )

    context = {
        "comparison": comparison,
    }

    return render(request, "players/confirm.html", context=context)


@login_required
def populate(request):
    """
    View Django responsável por popular o banco de dados
    com dados de um arquivo CSV.

    Args:
        request (HttpRequest): O objeto HttpRequest que representa
                                             a requisição HTTP recebida.

    Returns:
        HttpResponseRedirect: Um objeto HttpResponseRedirect que
                                              redireciona para a página inicial após a
                                              conclusão do processo de população do
                                              banco de dados.
    """
    with open("./dados.csv", encoding="utf-8") as dados_csv:
        reader = csv.reader(dados_csv)
        for row in reader:
            # jump header
            if row[0] == "Governor ID":
                continue

            jogador = Player.objects.filter(game_id=row[0]).first()

            if jogador is None:
                # create new player
                jogador = Player()
                jogador.game_id = row[0]
                jogador.nick = row[1]
                psa = Alliance.objects.filter(tag="PSA").first()
                jogador.alliance = psa
                jogador.save()
            else:
                # update some data
                oldnick = jogador.nick

                jogador.nick = row[2]
                if jogador.nick != oldnick:
                    if jogador.observacao:
                        jogador.observacao += (
                            f"\r\nMudança de nick: {oldnick} > {row[1]}"
                        )
                    else:
                        jogador.observacao = f"Mudança de nick: {oldnick} > {row[1]}"
                if not row[4] in ["32br", "32BR"]:
                    ally = Alliance.objects.filter(tag=row[4]).first()
                elif row[4] == "32br":
                    ally = Alliance.objects.get(pk=2)
                elif row[4] == "32BR":
                    ally = Alliance.objects.get(pk=1)
                else:
                    ally = None
                if ally is not None:
                    jogador.alliance = ally
                else:
                    nova = Alliance.objects.create(tag=row[4], nome=row[4])
                    nova.save()
                    if jogador.alliance.tag not in ["BNDS", "MIGR"]:
                        jogador.alliance = nova
                jogador.save()

            poder = row[3]
            if row[3] == "":
                poder = 0

            # Colunas de 5 a 9
            kills = []
            kills_t1 = row[5]
            if row[5] == "":
                kills_t1 = 0
            kills.append(kills_t1)
            kills_t2 = row[6]
            if row[6] == "":
                kills_t2 = 0
            kills.append(kills_t2)
            kills_t3 = row[7]
            if row[7] == "":
                kills_t3 = 0
            kills.append(kills_t3)
            kills_t4 = row[8]
            if row[8] == "":
                kills_t4 = 0
            kills.append(kills_t4)
            kills_t5 = row[9]
            if row[9] == "":
                kills_t5 = 0
            kills.append(kills_t5)

            killpoints = 0
            coeficientes = [0.2, 2, 4, 10, 20]
            for i, text in enumerate(kills):
                if isinstance(text, str):
                    if "." in text:
                        text = text.replace(".", "")
                    kills[i] = int(text)

                killpoints = killpoints + kills[i] * coeficientes[i]

            death = row[11]
            if row[11] == "":
                death = 0

            statusnovo = PlayerStatus()
            statusnovo.player = jogador
            statusnovo.data = cache.get("upload_date")
            if isinstance(poder, str):
                statusnovo.power = poder.replace(".", "")
            else:
                statusnovo.power = poder
            statusnovo.killpoints = killpoints
            if isinstance(death, str):
                statusnovo.deaths = death.replace(".", "")
            else:
                statusnovo.deaths = death

            statusnovo.killst4 = int(row[8].replace(".", ""))
            statusnovo.killst5 = int(row[9].replace(".", ""))

            statusnovo.save()

    return HttpResponseRedirect("/")


@login_required
def alliance(request, ally_id):
    """
    View responsável por exibir informações sobre uma aliança.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém os
                                             detalhes da requisição HTTP.
        ally_id (int): O ID da aliança a ser exibida.

    Returns:
        HttpResponse: O objeto HttpResponse que contém a resposta
                                HTTP com o conteúdo da página.

    Raises:
        Alliance.DoesNotExist: Se a aliança com o ID fornecido não existir.

    """
    ally = Alliance.objects.get(pk=ally_id)

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
                PlayerStatus.objects.filter(player=membro).order_by("-data").first()
            )
            if status:
                kills = kills + status.killpoints
                deaths = deaths + status.deaths
                power = power + status.power

        creditos = Credito.objects.filter(ally=ally).order_by("-timestamp")

        context = {
            "membros": pagina,
            "ally": ally,
            "total": len(membros),
            "kills": kills,
            "power": power,
            "death": deaths,
            "range": range(1, pagina.paginator.num_pages + 1),
            "creditos": creditos,
        }
        return render(request, "players/alianca.html", context)
    return render(request, "rise/404.html")


@login_required
def top300(request):
    """
    View que retorna os 300 jogadores com maior poder,
    excluindo aqueles da aliança "MIGR".

    Args:
        request (HttpRequest): O objeto HttpRequest que contém os
                                             detalhes da requisição HTTP.

    Returns:
        HttpResponse: O objeto HttpResponse que representa a resposta
                                HTTP com a lista dos 300 jogadores e o poder total.

    Raises:
        None
    """
    jogadores = []
    noreino = Player.objects.exclude(alliance__tag="MIGR")
    for jogador in noreino:
        status = PlayerStatus.objects.filter(player=jogador).order_by("-data").first()
        jogadores.append(status)
    jogadores.sort(key=lambda x: x.power if (x is not None) else 0, reverse=True)
    poder_total = 0
    for jogador in jogadores[:300]:
        poder_total = poder_total + jogador.power
    context = {
        "jogadores": jogadores[:300],
        "poder": poder_total,
    }
    return render(request, "players/top300.html", context=context)


@login_required
def falta_status(request, ally_id):
    """
    View que retorna os jogadores de uma aliança que não
    possuem status.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém
                                             os detalhes da requisição.
        ally_id (int): O ID da aliança.

    Returns:
        HttpResponse: O objeto HttpResponse que contém a resposta da view.
    """
    status = PlayerStatus.objects.all()
    id_quem_tem = []
    for cada in status:
        if cada.power != 0:
            id_quem_tem.append(cada.player.id)
    ally = Alliance.objects.get(pk=ally_id)
    jogadores_sem_status = Player.objects.filter(alliance=ally).exclude(
        id__in=id_quem_tem
    )

    context = {
        "players": jogadores_sem_status,
    }

    return render(request, "players/semstatus.html", context=context)


@login_required
def antigos(request, ally_id):
    """
    View que retorna os jogadores com status muito antigos
    de uma aliança.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém
                                             os detalhes da requisição HTTP.
        ally_id (int): O ID da aliança.

    Returns:
        HttpResponse: O objeto HttpResponse que contém a resposta
                                HTTP com a página renderizada.
    """
    status = PlayerStatus.objects.all()
    hoje = timezone.now()
    id_quem_tem = []
    for cada in status:
        diff = hoje - cada.data
        if diff.days < 15:
            id_quem_tem.append(cada.player.id)
    ally = Alliance.objects.get(pk=ally_id)
    jogadores_sem_status = Player.objects.filter(alliance=ally).exclude(
        id__in=id_quem_tem
    )

    context = {
        "players": jogadores_sem_status,
    }

    return render(request, "players/antigos.html", context=context)


@login_required
def edita_status(request, status_id):
    """
    View responsável por editar o status de um jogador.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém
                                             os dados da requisição.
        status_id (int): O ID do status a ser editado.

    Returns:
        HttpResponse: O objeto HttpResponse que representa a
                                resposta da requisição.

    Raises:
        None

    """
    if request.method == "POST":
        status = PlayerStatus.objects.all().filter(id=status_id).first()
        if status.editavel():
            status.power = request.POST["power"]
            status.killpoints = request.POST["killpoints"]
            status.deaths = request.POST["deaths"]
            status.data = timezone.now()
            status.save()
            logger.debug("%s editou %s", request.user.username, status.player.game_id)

        return redirect(f"/players/{status.player.game_id}")

    status = PlayerStatus.objects.all().filter(id=status_id).first()
    context = {"status": status}
    return render(request, "players/editastatus.html", context=context)


@login_required
def delete_status(request, status_id):
    """
    View responsável por deletar um status de jogador.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém
                                             os detalhes da requisição.
        status_id (int): O ID do status a ser deletado.

    Returns:
        HttpResponseRedirect: Um redirecionamento para a página
                                             de detalhes do jogo do jogador.

    Raises:
        None
    """
    status = PlayerStatus.objects.all().filter(id=status_id).first()
    if status.editavel():
        game_id = status.player.game_id
        status.delete()
        logger.debug("%s deletou status de %s", request.user.username, game_id)

    return redirect(f"/players/{status.player.game_id}")


def como_estou(request):
    """
    View responsável por exibir informações sobre o status do jogador em uma partida.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém os dados da requisição.

    Returns:
        HttpResponse: O objeto HttpResponse que contém a resposta da view.

    Raises:
        None
    """
    if request.method == "POST":
        kvk = Kvk.objects.filter(ativo=True).first()
        if not kvk:
            kvk = Kvk.objects.all().order_by("-inicio").first()

        inicio, final = get_datas(kvk)

        player_id = request.POST["game_id"]
        o_player = Player.objects.filter(game_id=player_id).first()
        status = (
            PlayerStatus.objects.filter(player=o_player)
            .filter(data__gte=inicio, data__lte=final)
            .order_by("data")
        )

        zerado = False
        if Zerado.objects.filter(kvk=kvk, player=o_player).first():
            zerado = True

        zerados = Zerado.objects.filter(kvk=kvk)
        zerados_lista = []
        for zerado_pra_lista in zerados:
            zerados_lista.append(zerado_pra_lista.player)

        banidos_e_inativos = Player.objects.filter(
            status__in=["BANIDO", "MIGROU", "INATIVO"]
        )

        primeiro = status.first()
        ultimo = status.last()

        status_kp = (
            PlayerStatus.objects.filter(data__gte=inicio, data__lte=final)
            .values("player__nick", "player__game_id")
            .annotate(
                kp=Max("killpoints") - Min("killpoints"),
                dt=Max("deaths") - Min("deaths"),
            )
            .order_by("-kp")
        )
        pos_kp = 1
        for stat in status_kp:
            if stat["player__game_id"] != ultimo.player.game_id:
                pos_kp = pos_kp + 1
            else:
                break

        status_dt = (
            PlayerStatus.objects.exclude(player__in=zerados_lista)
            .filter(data__gte=inicio, data__lte=final)
            .values("player__nick", "player__game_id")
            .annotate(
                kp=Max("killpoints") - Min("killpoints"),
                dt=Max("deaths") - Min("deaths"),
            )
            .order_by("-dt")
        )
        pos_dt = 1
        for stat in status_dt:
            if stat["player__game_id"] != ultimo.player.game_id:
                pos_dt = pos_dt + 1
            else:
                break

        faixa_inicio, faixa_fim = get_minha_faixa(primeiro.power)

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
                if stat.data.hour == primeiro.data.hour:
                    players_faixa_original.append(stat.player)

        status_kp_similares = (
            PlayerStatus.objects.all()
            .exclude(player__in=banidos_e_inativos)
            .exclude(player__in=zerados_lista)
            .filter(player__in=players_faixa_original)
            .filter(data__gte=inicio, data__lte=final)
            .values("player__nick", "player__game_id")
            .annotate(
                kp=Max("killpoints") - Min("killpoints"),
                dt=Max("deaths") - Min("deaths"),
            )
            .order_by("-kp")
        )
        status_dt_similares = (
            PlayerStatus.objects.all()
            .exclude(player__in=banidos_e_inativos)
            .exclude(player__in=zerados_lista)
            .filter(player__in=players_faixa_original)
            .filter(data__gte=inicio, data__lte=final)
            .values("player__nick", "player__game_id")
            .annotate(
                kp=Max("killpoints") - Min("killpoints"),
                dt=Max("deaths") - Min("deaths"),
            )
            .order_by("-dt")
        )

        todos_kp = len(status_kp_similares)
        pos_kp_faixa = todos_kp
        media_kp = 0
        continue_contando = True
        for stat in status_kp_similares:
            quem_eh = Player.objects.filter(game_id=stat["player__game_id"]).first()
            abate_mge = PontosDeMGE.objects.filter(kvk=kvk, player=quem_eh)
            abater = 0
            for pontos in abate_mge:
                abater = abater + pontos.pontos
            media_kp = media_kp + stat["kp"] - abater
            if stat["player__game_id"] != ultimo.player.game_id:
                if continue_contando:
                    pos_kp_faixa = pos_kp_faixa - 1
            else:
                continue_contando = False
        media_kp = int(media_kp / len(status_kp_similares))

        todos_dt = len(status_dt_similares)
        pos_dt_faixa = todos_dt
        media_mortes = 0
        continue_contando = True
        for stat in status_dt_similares:
            media_mortes = media_mortes + stat["dt"]
            if stat["player__game_id"] != ultimo.player.game_id:
                if continue_contando:
                    pos_dt_faixa = pos_dt_faixa - 1
            else:
                continue_contando = False
        media_mortes = int(media_mortes / len(status_dt_similares))

        context = {
            "kvk": kvk,
            "nick": ultimo.player.nick,
            "player_id": ultimo.player.game_id,
            "primeirostatus": primeiro,
            "atualizado": ultimo.data,
            "killpoints": ultimo.killpoints - primeiro.killpoints,
            "deaths": ultimo.deaths - primeiro.deaths,
            "power": (ultimo.power - primeiro.power) * -1,
            "perdeuganhou": "Ganhou" if ultimo.power > primeiro.power else "Perdeu",
            "poskp": pos_kp,
            "posdt": pos_dt,
            "todoskp": todos_kp,
            "poskpfaixa": pos_kp_faixa,
            "todosdt": todos_dt,
            "posdtfaixa": pos_dt_faixa,
            "comparadoa": players_faixa_original,
            "metamortes": media_mortes <= ultimo.deaths - primeiro.deaths,
            "mediamortes": media_mortes,
            "metakp": media_kp <= ultimo.killpoints - primeiro.killpoints,
            "mediakp": media_kp,
            "zerado": zerado,
        }

        return render(request, "players/emkvk.html", context=context)
    return render(request, "rise/404.html")


@login_required
def criar_advertencia(request):
    """
    Cria uma advertência para um jogador com base
    nos dados recebidos via requisição POST.

    Args:
        request (HttpRequest): O objeto HttpRequest contendo
                                             os dados da requisição.

    Returns:
        HttpResponseRedirect: Redireciona para a página de advertências
                                             dos jogadores.

    Raises:
        None
    """
    player = Player.objects.filter(game_id=request.POST["game_id"]).first()

    if player:
        adv = Advertencia()
        adv.player = player
        adv.duracao = request.POST["duracao"]

        if request.POST["tipo"] == "mge":
            limite = 7000000
            faixa = (int(request.POST["pontuacao"]) - limite) // 1000000 or 1
            adv.descricao = (
                f"quebrou limite em MGE | Multa: {faixa*5}M comida,  "
                f"{faixa*5}M madeira, {faixa*5}M pedra, {faixa*10}M ouro"
            )

            mge = Mge.objects.order_by("-id").first()

            apunir = Punido()
            apunir.mge = mge
            apunir.player = player
            apunir.save()
            logger.debug(
                "%s puniu %s no %s", request.user.username, player.game_id, mge
            )
        elif request.POST["tipo"] == "poder":
            limite = 150000
            faixa = (int(request.POST["pontuacao"]) - limite) // 50000 or 1
            adv.descricao = (
                f"quebrou limite em Evento de Poder | Multa: {faixa*25}M comida,  "
                f"{faixa*25}M madeira, {faixa*25}M pedra, {faixa*50}M ouro"
            )
        else:
            limite = 36000
            faixa = (int(request.POST["pontuacao"]) - limite) // 10000 or 1
            adv.descricao = (
                f"quebrou limite em Evento de Acelerador | Multa: {faixa*25}"
                f"M comida,  {faixa*25}M madeira, {faixa*25}M pedra, {faixa*50}M ouro"
            )

        adv.save()
        logger.debug("%s advertiu %s", request.user.username, adv.player.game_id)

        return redirect("/players/advertencias")
    return render(request, "rise/404.html")


def advertencias(request):
    """
    View que retorna a página de advertências.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém
                                             os detalhes da requisição.

    Returns:
        HttpResponse: O objeto HttpResponse que representa a resposta
                                da página de advertências.
    """
    advs = Advertencia.objects.all().order_by("-inicio")

    validas = []
    vencidas = []
    for adv in advs:
        if adv.is_restrito():
            validas.append(adv)
        else:
            vencidas.append(adv)

    context = {
        "advertencias": validas,
        "vencidas": vencidas,
    }

    return render(request, "players/advertencias.html", context=context)


@login_required
def zerou_banido(request, player_id):
    """
    View que registra a ação de zerar um jogador banido.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém os
                                             detalhes da requisição.
        player_id (int): O ID do jogador a ser zerado.

    Returns:
        HttpResponseRedirect: Redireciona para a página de detalhes do jogador.

    Raises:
        Player.DoesNotExist: Se o jogador com o ID fornecido não existir.

    """
    player = Player.objects.get(game_id=player_id)

    if player:
        hoje = timezone.now().strftime("%d/%m/%Y")

        player.observacao = (
            player.observacao + "\r\n" + f"Zerado por {request.user.username} em {hoje}"
        )

        player.save()

    return redirect(f"/players/{player_id}")


@login_required
def append_farm(request, principal_id):
    """
    View responsável por adicionar uma fazenda ao jogador principal.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém os dados da requisição.
        principal_id (int): O ID do jogador principal.

    Returns:
        HttpResponseRedirect: Redireciona para a página de
                                             detalhes do jogador principal.

    Raises:
        Player.DoesNotExist: Se o jogador principal não for encontrado.
    """
    principal = Player.objects.get(game_id=principal_id)
    if request.method == "POST":
        form = AddFarmForm(request.POST)
        if form.is_valid():
            farm_id = form.cleaned_data["farm"]

            farm = Player.objects.get(game_id=farm_id)

            principal.farms.add(farm)

            principal.save()
    return redirect(f"/players/{principal_id}/")


def remove_farm(request, player_id, farm_id):
    """
    Remove uma fazenda de um jogador.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.
        player_id (int): O ID do jogador.
        farm_id (int): O ID da fazenda a ser removida.

    Returns:
        HttpResponseRedirect: Um redirecionamento para a página de
                                             detalhes do jogador.
    """
    player = Player.objects.get(game_id=player_id)
    farm = Player.objects.get(game_id=farm_id)

    player.farms.remove(farm)
    player.save()

    return redirect(f"/players/{player_id}/")
