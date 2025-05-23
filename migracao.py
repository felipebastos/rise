from django.contrib.auth.models import User

from bank.models import Donation, Semana
from kvk.models import AdicionalDeFarms, Etapas, Kvk, Zerado
from mge.models import Comandante, EventoDePoder, Inscrito, Mge, Punido, Ranking
from players.models import Advertencia, Alliance, Player, PlayerStatus


def migrar(items):
    for obj in items:
        obj.save(using="kingdom")


def transferir():
    print("Inserindo os usuários do site.")
    objlist = User.objects.using("default").all()
    migrar(objlist)
    print("Inserindo as Alianças do site.")
    objlist = Alliance.objects.using("default").all()
    migrar(objlist)
    print("Inserindo os Jogadores do site.")
    objlist = Player.objects.using("default").all()
    migrar(objlist)
    print("Inserindo os Status dos jogadores do site.")
    objlist = PlayerStatus.objects.using("default").all()
    migrar(objlist)
    print("Inserindo as Advertências do site.")
    objlist = Advertencia.objects.using("default").all()
    migrar(objlist)
    print("Inserindo as Semanas de doação do site.")
    objlist = Semana.objects.using("default").all()
    migrar(objlist)
    print("Inserindo as Doações do site.")
    objlist = Donation.objects.using("default").all()
    migrar(objlist)
    print("Inserindo os KvKs do site.")
    objlist = Kvk.objects.using("default").all()
    migrar(objlist)
    print("Inserindo os Zerados em KvK do site.")
    objlist = Zerado.objects.using("default").all()
    migrar(objlist)
    print("Inserindo os Dados de farms em KvK do site.")
    objlist = AdicionalDeFarms.objects.using("default").all()
    migrar(objlist)
    print("Inserindo as Etapas de KvK do site.")
    objlist = Etapas.objects.using("default").all()
    migrar(objlist)
    print("Inserindo os MGEs do site.")
    objlist = Mge.objects.using("default").all()
    migrar(objlist)
    print("Inserindo os Punidos em MGE do site.")
    objlist = Punido.objects.using("default").all()
    migrar(objlist)
    print("Inserindo os Rankings de MGE do site.")
    objlist = Ranking.objects.using("default").all()
    migrar(objlist)
    print("Inserindo os Inscritos em MGE do site.")
    objlist = Inscrito.objects.using("default").all()
    migrar(objlist)
    print("Inserindo os Comandantes do jogo do site.")
    objlist = Comandante.objects.using("default").all()
    migrar(objlist)
    print("Inserindo os Punidos em Evento de Poder do site.")
    objlist = EventoDePoder.objects.using("default").all()
    migrar(objlist)
