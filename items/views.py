from django.shortcuts import redirect, render

from items.forms import PedidoForm
from items.models import Pedido
from players.models import Player


# Create your views here.
def home(request):
    form = PedidoForm(request.POST or None)
    confirma = ""
    if request.method == "POST":
        if form.is_valid():
            player = Player.objects.filter(
                game_id=form.cleaned_data["player"]
            ).first()
            if player:
                novo = Pedido()
                novo.player = player
                novo.item = form.cleaned_data["item"]
                novo.quantidade = form.cleaned_data["quantidade"]
                novo.save()
                confirma = "Seu pedido foi registrado com sucesso!"

    form = PedidoForm()
    pedidos_pendentes = Pedido.objects.filter(avaliado=False).order_by(
        "pedido_em"
    )
    pedidos_avaliados = Pedido.objects.filter(avaliado=True).order_by(
        "pedido_em"
    )
    context = {
        "form": form,
        "pendentes": pedidos_pendentes,
        "avaliados": pedidos_avaliados,
        "confirma": confirma,
    }
    return render(request, "items/index.html", context=context)


def aprovar(request, pedido_id):
    pedido = Pedido.objects.get(pk=pedido_id)
    pedido.avaliado = True
    pedido.aprovado = True
    pedido.save()
    return redirect("/items/")


def reprovar(request, pedido_id):
    pedido = Pedido.objects.get(pk=pedido_id)
    pedido.avaliado = True
    pedido.save()
    return redirect("/items/")


def cancelar_avaliacao(request, pedido_id):
    pedido = Pedido.objects.get(pk=pedido_id)
    pedido.avaliado = False
    pedido.aprovado = False
    pedido.save()
    return redirect("/items/")
