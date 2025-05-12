from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from ghevent.forms import EventoGHForm, InscritoGHForm
from ghevent.models import EventoGH, InscritoGH
from players.models import Player


# Create your views here.
def home(request):
    form = EventoGHForm()
    todos = EventoGH.objects.all()
    context = {
        "form": form,
        "eventos": todos,
    }
    return render(request, "ghevent/index.html", context=context)


def event(request, idi):
    form = InscritoGHForm()
    evento = EventoGH.objects.get(pk=idi)
    inscritos = InscritoGH.objects.filter(evento=evento)
    context = {
        "form": form,
        "event": evento,
        "inscritos": inscritos,
    }
    return render(request, "ghevent/ghevent.html", context=context)


@login_required
def startnewgh(request):
    if request.method == "POST":
        form = EventoGHForm(request.POST)
        if form.is_valid():
            novo_evento = form.save()
            return redirect(f"/gh/{novo_evento.id}/")
    return redirect("/gh/")


@login_required
def add_inscrito_gh(request, idi):
    if request.method == "POST":
        form = InscritoGHForm(request.POST)
        if form.is_valid():
            novo_inscrito_id = form.cleaned_data.get("busca")
            inscrito = Player.objects.get(game_id=novo_inscrito_id)
            evento = EventoGH.objects.get(pk=idi)
            inscricao = InscritoGH()
            inscricao.player = inscrito
            inscricao.evento = evento
            inscricao.save()
            return redirect(f"/gh/{idi}/")
    return redirect("/gh/")


@login_required
def remove_inscrito_gh(request, idi, eid):
    inscrito = InscritoGH.objects.get(pk=eid)
    inscrito.delete()
    return redirect(f"/gh/{idi}/")
