from django import template

from players.models import Alliance

register = template.Library()


@register.filter
def alliances(req):
    return Alliance.objects.all().exclude(pk__in=[1, 2, 3])
