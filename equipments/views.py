from collections import OrderedDict

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from equipments.forms import (
    BuffFormSet,
    ConjuntoForm,
    EquipForm,
    EquipmentForm,
    SetBuffFormSet,
)
from equipments.models import Conjunto, Equipamento

# Create your views here.
PECAS = (
    ("cap", "capacete"),
    ("arm", "armamento"),
    ("pei", "peitoral"),
    ("luv", "luva"),
    ("ace", "ace"),
    ("cal", "calca"),
    ("acd", "acd"),
    ("bot", "botas"),
)


def home(request):
    equipform = EquipForm(request.GET or None)

    armadura = {}
    buffs_conjuntos = {}

    status_list = {}
    status_list["Status base: ataque"] = 0
    status_list["Status base: defesa"] = 0
    status_list["Status base: saúde"] = 0

    if equipform.is_valid():
        for peca in PECAS:
            armadura[peca[1]] = (
                equipform.cleaned_data[peca[1]] or Equipamento(),
                equipform.cleaned_data[f"{peca[0]}_spec"] or False,
                equipform.cleaned_data[f"{peca[0]}_icon"] or False,
            )
            if equipform.cleaned_data[f"{peca[0]}_icon"]:
                match (peca[0]):
                    case ("cap"):
                        status_list["Status base: defesa"] = (
                            status_list["Status base: defesa"]
                            + 3
                            + (
                                1
                                if equipform.cleaned_data[f"{peca[0]}_spec"]
                                else 0
                            )
                        )
                    case ("pei"):
                        status_list["Status base: defesa"] = (
                            status_list["Status base: defesa"]
                            + 3
                            + (
                                1
                                if equipform.cleaned_data[f"{peca[0]}_spec"]
                                else 0
                            )
                        )
                    case ("arm"):
                        status_list["Status base: ataque"] = (
                            status_list["Status base: ataque"]
                            + 3
                            + (
                                1
                                if equipform.cleaned_data[f"{peca[0]}_spec"]
                                else 0
                            )
                        )
                    case ("luv"):
                        status_list["Status base: ataque"] = (
                            status_list["Status base: ataque"]
                            + 3
                            + (
                                1
                                if equipform.cleaned_data[f"{peca[0]}_spec"]
                                else 0
                            )
                        )
                    case ("cal"):
                        status_list["Status base: saúde"] = (
                            status_list["Status base: saúde"]
                            + 3
                            + (
                                1
                                if equipform.cleaned_data[f"{peca[0]}_spec"]
                                else 0
                            )
                        )
                    case ("bot"):
                        status_list["Status base: saúde"] = (
                            status_list["Status base: saúde"]
                            + 3
                            + (
                                1
                                if equipform.cleaned_data[f"{peca[0]}_spec"]
                                else 0
                            )
                        )
                    case ("ace"):
                        status_list["Status base: saúde"] = (
                            status_list["Status base: saúde"]
                            + 3
                            + (
                                1
                                if equipform.cleaned_data[f"{peca[0]}_spec"]
                                else 0
                            )
                        )
                    case ("acd"):
                        status_list["Status base: saúde"] = (
                            status_list["Status base: saúde"]
                            + 3
                            + (
                                1
                                if equipform.cleaned_data[f"{peca[0]}_spec"]
                                else 0
                            )
                        )

    lista = []
    for k, peca in armadura.items():
        lista.append(peca[0])
    for conj in Conjunto.objects.all():
        has_buffs = conj.get_buffs(lista)
        if has_buffs:
            buffs_conjuntos[conj.nome] = has_buffs

    buffs = {}

    for i, item in armadura.items():
        if item[0].pk:
            for status in item[0].buffs.all():
                label = f"{status.get_status_display()} de {status.get_spec_display()}"
                if status.ativacao < 1:
                    label = f"{label} ({status.ativacao*100}%)"
                if label not in buffs:
                    buffs[label] = (
                        round((status.valor * (1.3 if item[1] else 1)) * 2) / 2
                    )
                else:
                    buffs[label] = buffs[label] + round(
                        (status.valor * (1.3 if item[1] else 1) * 2) / 2
                    )

    lista = {}
    for key, item in armadura.items():
        lista[key] = item[0]

    ordered_buffs = OrderedDict()

    key_list = sorted(buffs.keys())
    for key in key_list:
        ordered_buffs[key] = buffs[key]

    context = {
        "capform": equipform,
        "montagem": lista,
        "status": status_list,
        "buffs": ordered_buffs,
        "conjuntos": buffs_conjuntos,
    }

    return render(request, "equipments/index.html", context=context)


@login_required
def add_equip(request):
    if request.method == "POST":
        form = EquipmentForm(request.POST)

        instance = None
        if form.is_valid():
            instance = form.save()
            instance.miniatura = request.FILES["miniatura"]
            instance.save()
        buffform = BuffFormSet(request.POST, instance=instance)
        if buffform.is_valid():
            buffform.save()

    form = EquipmentForm()
    buffs = BuffFormSet()

    context = {
        "form": form,
        "buffform": buffs,
    }

    return render(request, "equipments/add.html", context=context)


@login_required
def conjuntos(request):
    form = ConjuntoForm()
    buffform = SetBuffFormSet()
    if request.method == "POST":
        form = ConjuntoForm(request.POST)

        instance = None
        if form.is_valid():
            instance = form.save()
        buffform = SetBuffFormSet(request.POST, instance=instance)
        if buffform.is_valid():
            buffform.save()

    context = {
        "form": form,
        "buffform": buffform,
    }
    return render(request, "equipments/conjuntos.html", context=context)
