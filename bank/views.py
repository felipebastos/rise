from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from bank.forms import CreditoForm
from bank.models import Credito, Donation, Semana
from players.models import Alliance, Player


# Create your views here.
@login_required
def index(request):
    semanas = Semana.objects.all()
    context = {"semanas": semanas}

    return render(request, "bank/index.html", context=context)


@login_required
def create_week(request, tag, resource):
    ally = Alliance.objects.filter(tag=tag)[0]

    jogadores = (
        Player.objects.all()
        .filter(alliance=ally)
        .exclude(rank="SA")
        .exclude(status="FARM")
    )

    semana = Semana()
    semana.recurso = resource
    semana.save()

    for jogador in jogadores:
        doacao_programada = Donation()
        doacao_programada.player = jogador
        doacao_programada.semana = semana
        doacao_programada.save()

    return redirect("/bank/")


@login_required
def week(request, weekid):
    semana = Semana.objects.get(id=weekid)

    doadores = Donation.objects.filter(semana=semana).order_by("donated")

    context = {
        "semana": semana,
        "doadores": doadores,
    }

    return render(request, "bank/week.html", context=context)


@login_required
def donated(request, donationid):
    doador = Donation.objects.get(id=donationid)

    doador.donated = not doador.donated

    doador.save()

    return redirect(f"/bank/week/{doador.semana.id}")


@login_required
def donations_report(request):
    context = {"devedores": Donation.objects.filter(donated=False).order_by("player")}
    return render(request, "bank/report.html", context=context)


@login_required
def register_week(request, weekid):
    if request.method == "POST":
        semana = Semana.objects.get(id=weekid)

        doadores = Donation.objects.filter(semana=semana)

        for doador in doadores:
            if doador.player.game_id in request.POST:
                doador.donated = True
                doador.save()
            else:
                doador.donated = False
                doador.save()

    return redirect(f"/bank/week/{weekid}")


@login_required
def add_credits(request):
    form = CreditoForm(request.POST or None)

    if form.is_valid():
        form.save()

    form = CreditoForm()

    creditos = Credito.objects.order_by("-timestamp")

    ultimos = {}

    for credito in creditos:
        if credito.ally.id not in ultimos:
            ultimos[credito.ally.id] = credito

    context = {
        "form": form,
        "creditos": ultimos,
    }

    return render(request, "bank/credits.html", context=context)
