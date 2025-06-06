from django.utils import timezone

from mge.models import Inscrito, Punido, Ranking
from players.models import PlayerStatus


def corrigir_datetime_naive():
    for modelo in [Inscrito, Punido, Ranking]:
        for obj in modelo.objects.all():
            if timezone.is_naive(obj.inserido):
                obj.inserido = timezone.make_aware(
                    obj.inserido, timezone.get_default_timezone()
                )
                obj.save()
                print("Uma data foi corrigida.")
    for obj in PlayerStatus.objects.all():
        if timezone.is_naive(obj.data):
            obj.data = timezone.make_aware(obj.data, timezone.get_default_timezone())
            obj.save()
            print("Um status foi corrigido.")
