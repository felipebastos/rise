from django import template
from kvk.models import Cargo

from players.models import Alliance

register = template.Library()


@register.filter
def alliances(req):
    return Alliance.objects.all().exclude(pk__in=[1, 2, 3])


@register.filter
def has_cargos(player_nick: str):
    cargos = Cargo.objects.filter(player__nick=player_nick)

    return cargos
