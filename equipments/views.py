from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from equipments.forms import BuffFormSet, EquipForm, EquipmentForm
from equipments.models import Equipamento

# Create your views here.
def home(request):
    equipform = EquipForm(request.GET or None)

    armadura = {}

    if equipform.is_valid():
        armadura["capacete"] = (
            equipform.cleaned_data["capacete"] or Equipamento(),
            equipform.cleaned_data["cap_spec"] or False,
            equipform.cleaned_data["cap_icon"] or False,
        )
        armadura["armamento"] = (
            equipform.cleaned_data["armamento"] or Equipamento(),
            equipform.cleaned_data["arm_spec"] or False,
            equipform.cleaned_data["arm_icon"] or False,
        )
        armadura["peitoral"] = (
            equipform.cleaned_data["peitoral"] or Equipamento(),
            equipform.cleaned_data["pei_spec"] or False,
            equipform.cleaned_data["pei_icon"] or False,
        )
        armadura["luva"] = (
            equipform.cleaned_data["luva"] or Equipamento(),
            equipform.cleaned_data["luv_spec"] or False,
            equipform.cleaned_data["luv_icon"] or False,
        )
        armadura["ace"] = (
            equipform.cleaned_data["ace"] or Equipamento(),
            equipform.cleaned_data["ace_spec"] or False,
            equipform.cleaned_data["ace_icon"] or False,
        )
        armadura["calca"] = (
            equipform.cleaned_data["calca"] or Equipamento(),
            equipform.cleaned_data["cal_spec"] or False,
            equipform.cleaned_data["cal_icon"] or False,
        )
        armadura["acd"] = (
            equipform.cleaned_data["acd"] or Equipamento(),
            equipform.cleaned_data["acd_spec"] or False,
            equipform.cleaned_data["acd_icon"] or False,
        )
        armadura["botas"] = (
            equipform.cleaned_data["botas"] or Equipamento(),
            equipform.cleaned_data["bot_spec"] or False,
            equipform.cleaned_data["bot_icon"] or False,
        )

    status_list = {}
    for i, item in armadura.items():
        if item[0].pk:
            for status in item[0].buffs.all():
                if (
                    f"{status.get_status_display()} de {status.get_spec_display()}"
                    not in status_list
                ):
                    status_list[
                        f"{status.get_status_display()} de {status.get_spec_display()}"
                    ] = status.valor * (1.3 if item[1] else 1)
                else:
                    status_list[
                        f"{status.get_status_display()} de {status.get_spec_display()}"
                    ] = status_list[
                        f"{status.get_status_display()} de {status.get_spec_display()}"
                    ] + status.valor * (
                        1.3 if item[1] else 1
                    )

    lista = {}
    for key, item in armadura.items():
        lista[key] = item[0]

    context = {
        "capform": equipform,
        "montagem": lista,
        "status": status_list,
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
