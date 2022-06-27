from django import template
from mge.models import EventoDePoder, Inscrito, Punido

register = template.Library()


@register.filter
def getPunicoes(insc : Inscrito):
    return Punido.objects.filter(player=insc.player)

@register.filter
def temPunicoes(insc : Inscrito):
    if len(Punido.objects.filter(player=insc.player)) > 0 or len(EventoDePoder.objects.filter(player=insc.player)) > 0:
        return True
    return False

@register.filter
def getPunicoesPoder(insc: Inscrito):
    return EventoDePoder.objects.filter(player=insc.player)
