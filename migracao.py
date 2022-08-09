from django.contrib.auth.models import User

from players.models import Alliance, Player, PlayerStatus, Advertencia
from bank.models import Semana, Donation
from kvk.models import Kvk, Zerado, AdicionalDeFarms, Etapas
from mge.models import Mge, Punido, Ranking, Inscrito, Comandante, EventoDePoder

def migrar(items):
    for obj in items:
        obj.save(using='mysql')

def transferir():
    objlist = User.objects.using('default').all()
    migrar(objlist)
    
    objlist = Alliance.objects.using('default').all()
    migrar(objlist)
    
    objlist = Player.objects.using('default').all()
    migrar(objlist)
    
    objlist = PlayerStatus.objects.using('default').all()
    migrar(objlist)
    
    objlist = Advertencia.objects.using('default').all()
    migrar(objlist)
    
    objlist = Semana.objects.using('default').all()
    migrar(objlist)
    
    objlist = Donation.objects.using('default').all()
    migrar(objlist)
    
    objlist = Kvk.objects.using('default').all()
    migrar(objlist)
    
    objlist = Zerado.objects.using('default').all()
    migrar(objlist)
    
    objlist = AdicionalDeFarms.objects.using('default').all()
    migrar(objlist)
    
    objlist = Etapas.objects.using('default').all()
    migrar(objlist)
    
    objlist = Mge.objects.using('default').all()
    migrar(objlist)
    
    objlist = Punido.objects.using('default').all()
    migrar(objlist)
    
    objlist = Ranking.objects.using('default').all()
    migrar(objlist)
    
    objlist = Inscrito.objects.using('default').all()
    migrar(objlist)
    
    objlist = Comandante.objects.using('default').all()
    migrar(objlist)
    
    objlist = EventoDePoder.objects.using('default').all()
    migrar(objlist)