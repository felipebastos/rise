from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from osiris.forms import ArcaForm, MarchaForm, TimeForm
from osiris.models import Funcao, Marcha, Time


# Create your views here.
def home(request):
    arca = ArcaForm(request.POST or None)

    if request.method == "POST":
        if arca.is_valid():
            arca.save()

    context = {
        "arcaform": arca,
        "times": Time.objects.all(),
    }

    return render(request, "osiris/index.html", context=context)


def editar_time(request, timeid):
    time_form = TimeForm(request.POST or None)

    time = Time.objects.get(pk=timeid)

    if time_form.is_valid():
        funcao = Funcao()
        funcao.player = time_form.cleaned_data.get("player")
        funcao.lado = time_form.cleaned_data.get("lado")
        funcao.save()

        time.funcoes.add(funcao)

        time.save()

    context = {
        "timeform": time_form,
        "time_a": Funcao.objects.filter(time__pk=timeid, lado="a"),
        "time_b": Funcao.objects.filter(time__pk=timeid, lado="b"),
    }

    return render(request, "osiris/time.html", context=context)


@login_required
def configurar_marchas(request, funcaoid):
    marchaform = MarchaForm(request.POST or None)

    funcao = Funcao.objects.get(pk=funcaoid)

    if marchaform.is_valid():
        if len(funcao.marchas.all()) < 5:
            marcha = marchaform.save()

            funcao.marchas.add(marcha)
            funcao.save()

    context = {
        "marchaform": marchaform,
        "funcao": funcao,
        "time": funcao.time_set.first().id,
    }

    return render(request, "osiris/marchas.html", context=context)


@login_required
def remove_marcha(request, marchaid):
    marcha = Marcha.objects.get(pk=marchaid)
    funcao_id = marcha.funcao_set.first().id
    marcha.delete()

    return HttpResponseRedirect(f"/osiris/marchas/{funcao_id}/")


@login_required
def remove_funcao(request, funcaoid):
    funcao = Funcao.objects.get(pk=funcaoid)
    timeid = funcao.time_set.first().id

    funcao.delete()

    return HttpResponseRedirect(f"/osiris/time/{timeid}/")
