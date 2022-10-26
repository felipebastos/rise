from django.shortcuts import render

from equipments.forms import BuffFormSet, EquipForm, EquipmentForm
from equipments.models import Equipamento

# Create your views here.
def home(request):

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
    equipform = EquipForm(request.GET or None)

    armadura = {}

    if equipform.is_valid():
        armadura["capacete"] = (
            equipform.cleaned_data["capacete"] or Equipamento()
        )
        armadura["armamento"] = (
            equipform.cleaned_data["armamento"] or Equipamento()
        )
        armadura["peitoral"] = (
            equipform.cleaned_data["peitoral"] or Equipamento()
        )
        armadura["luva"] = equipform.cleaned_data["luva"] or Equipamento()
        armadura["ace"] = equipform.cleaned_data["ace"] or Equipamento()
        armadura["calca"] = equipform.cleaned_data["calca"] or Equipamento()
        armadura["acd"] = equipform.cleaned_data["acd"] or Equipamento()
        armadura["botas"] = equipform.cleaned_data["botas"] or Equipamento()

    status_list = {}
    for i, item in armadura.items():
        if item.pk:
            for status in item.buffs.all():
                if (
                    f"{status.get_status_display()} de {status.get_spec_display()}"
                    not in status_list
                ):
                    status_list[
                        f"{status.get_status_display()} de {status.get_spec_display()}"
                    ] = status.valor
                else:
                    status_list[
                        f"{status.get_status_display()} de {status.get_spec_display()}"
                    ] = (
                        status_list[
                            f"{status.get_status_display()} de {status.get_spec_display()}"
                        ]
                        + status.valor
                    )

    context = {
        "form": form,
        "buffform": buffs,
        "capform": equipform,
        "montagem": armadura,
        "status": status_list,
    }

    return render(request, "equipments/index.html", context=context)
