"""Funções úteis sobre datas."""

from django.utils import timezone


def get_datas(kvk):
    """Retorna os inícios e finais de um kvk."""
    inicio = kvk.inicio
    if kvk.primeira_luta:
        inicio = kvk.primeira_luta

    final = kvk.final
    if not final:
        final = timezone.now()

    return inicio, final
