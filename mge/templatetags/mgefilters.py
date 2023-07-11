from datetime import datetime

from django import template
from django.utils import timezone

from kvk.models import Consolidado, Kvk
from mge.models import EventoDePoder, Inscrito, Punido

register = template.Library()


@register.filter
def getPunicoes(insc: Inscrito):
    limite = timezone.make_aware(datetime.fromisoformat("2022-07-03"))
    return Punido.objects.filter(inserido__gte=limite).filter(player=insc.player)


@register.filter
def temPunicoes(insc: Inscrito):
    limite = timezone.make_aware(datetime.fromisoformat("2022-07-03"))

    if (
        len(Punido.objects.filter(inserido__gte=limite).filter(player=insc.player)) > 0
        or len(
            EventoDePoder.objects.filter(inserido__gte=limite).filter(
                player=insc.player
            )
        )
        > 0
    ):
        return True
    return False


@register.filter
def getPunicoesPoder(insc: Inscrito):
    limite = timezone.make_aware(datetime.fromisoformat("2022-07-03"))
    return EventoDePoder.objects.filter(inserido__gte=limite).filter(player=insc.player)


@register.filter
def is_consolidado(insc: Inscrito):
    kvk = (
        Kvk.objects.filter(ativo=False)
        .filter(final__lte=insc.inserido)
        .order_by("-inicio")
        .first()
    )
    consolidado = Consolidado.objects.filter(
        player__game_id=insc.player.game_id, kvk=kvk
    ).first()

    if consolidado:
        return True
    return False


@register.filter
def get_posicao(insc: Inscrito):
    kvk = (
        Kvk.objects.filter(ativo=False)
        .filter(final__lte=insc.inserido)
        .order_by("-inicio")
        .first()
    )
    consolidado = Consolidado.objects.filter(
        player__game_id=insc.player.game_id, kvk=kvk
    ).first()

    if consolidado:
        return consolidado.posicao_dt
    return 0


@register.filter
def get_cor(insc: Inscrito):
    kvk = (
        Kvk.objects.filter(ativo=False)
        .filter(final__lte=insc.inserido)
        .order_by("-inicio")
        .first()
    )
    consolidado = Consolidado.objects.filter(
        player__game_id=insc.player.game_id, kvk=kvk
    ).first()

    if consolidado:
        return consolidado.cor_dt
    return 0
