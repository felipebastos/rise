from django.contrib.auth.models import User

from players.models import Alliance, Player, PlayerStatus, Advertencia
from bank.models import Semana, Donation
from kvk.models import Kvk, Zerado, AdicionalDeFarms, Etapas
from mge.models import Mge, Punido, Ranking, Inscrito, Comandante, EventoDePoder

def migrar(items):
    for obj in items:
        obj.save(using='kingdom')

def transferir():
    print('Inserindo os usuários do site.')
    objlist = User.objects.using('default').all()
    migrar(objlist)
    print('Inserindo as Alianças do site.')
    objlist = Alliance.objects.using('default').all()
    migrar(objlist)
    print('Inserindo os Jogadores do site.')
    objlist = Player.objects.using('default').all()
    for obj in objlist:
        novo = Player()
        novo.nick = obj.nick
        novo.alliance = obj.alliance
        novo.rank = obj.rank
        novo.specialty = obj.specialty
        novo.status = obj.status
        novo.observacao = obj.observacao
        novo.alterado_em = obj.alterado_em
        novo.alterado_por = obj.alterado_por
        novo.save(using='kingdom')
    print('Inserindo os Status dos jogadores do site.')
    objlist = PlayerStatus.objects.using('default').all()
    for obj in objlist:
        novo = PlayerStatus()
        novo.player = obj.player
        novo.data = obj.data
        novo.power = obj.power
        novo.killpoints = obj.killpoints
        novo.deaths = obj.deaths
        novo.save()
    print('Inserindo as Advertências do site.')
    objlist = Advertencia.objects.using('default').all()
    for obj in objlist:
        nova = Advertencia()
        nova.player = obj.player
        nova.inicio = obj.inicio
        nova.duracao = obj.duracao
        obj.descricao = obj.descricao
        nova.save()
    print('Inserindo as Semanas de doação do site.')
    objlist = Semana.objects.using('default').all()
    migrar(objlist)
    print('Inserindo as Doações do site.')
    objlist = Donation.objects.using('default').all()
    migrar(objlist)
    print('Inserindo os KvKs do site.')
    objlist = Kvk.objects.using('default').all()
    migrar(objlist)
    print('Inserindo os Zerados em KvK do site.')
    objlist = Zerado.objects.using('default').all()
    migrar(objlist)
    print('Inserindo os Dados de farms em KvK do site.')
    objlist = AdicionalDeFarms.objects.using('default').all()
    migrar(objlist)
    print('Inserindo as Etapas de KvK do site.')
    objlist = Etapas.objects.using('default').all()
    for obj in objlist:
        nova = Etapas()
        nova.kvk = obj.kvk
        nova.date = obj.date
        nova.descricao = obj.descricao
        nova.save()
    print('Inserindo os MGEs do site.')
    objlist = Mge.objects.using('default').all()
    migrar(objlist)
    print('Inserindo os Punidos em MGE do site.')
    objlist = Punido.objects.using('default').all()
    migrar(objlist)
    print('Inserindo os Rankings de MGE do site.')
    objlist = Ranking.objects.using('default').all()
    migrar(objlist)
    print('Inserindo os Inscritos em MGE do site.')
    objlist = Inscrito.objects.using('default').all()
    migrar(objlist)
    print('Inserindo os Comandantes do jogo do site.')
    objlist = Comandante.objects.using('default').all()
    migrar(objlist)
    print('Inserindo os Punidos em Evento de Poder do site.')
    objlist = EventoDePoder.objects.using('default').all()
    migrar(objlist)