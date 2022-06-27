from django import template
from mge.models import Inscrito, Punido

register = template.Library()


@register.filter
def getPunicoes(insc : Inscrito):
    print(Punido.objects.filter(player=insc.player))
    return Punido.objects.filter(player=insc.player)

@register.filter
def temPunicoes(insc : Inscrito):
    if len(Punido.objects.filter(player=insc.player)) > 0:
        return True
    return False
