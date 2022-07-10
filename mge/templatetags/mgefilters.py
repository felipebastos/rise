from datetime import datetime
from django import template
from mge.models import EventoDePoder, Inscrito, Punido
from django.utils import timezone

register = template.Library()


@register.filter
def getPunicoes(insc : Inscrito):
    return Punido.objects.filter(player=insc.player)

@register.filter
def temPunicoes(insc : Inscrito):
    limite = timezone.make_aware(datetime.fromisoformat('2022-07-03'))
    
    if len(Punido.objects.filter(inserido__gte=limite).filter(player=insc.player)) > 0 or len(EventoDePoder.objects.filter(inserido__gte=limite).filter(player=insc.player)) > 0:
        return True
    return False

@register.filter
def getPunicoesPoder(insc: Inscrito):
    return EventoDePoder.objects.filter(player=insc.player)
