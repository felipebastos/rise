from typing import Dict
from django import template

from kvk.models import Cargo

register = template.Library()


@register.filter
def get(dic: Dict, key):
    return dic[key]


@register.filter
def foi_rali(player_nick: str, kvkid):
    tem = Cargo.objects.filter(
        player__nick=player_nick, kvk__id=kvkid, funcao="ral"
    )

    if tem:
        return "ral"
    return ""


@register.filter
def foi_guarnicao(player_nick: str, kvkid):
    tem = Cargo.objects.filter(
        player__nick=player_nick, kvk__id=kvkid, funcao="gua"
    )

    if tem:
        return "gua"
    return ""
