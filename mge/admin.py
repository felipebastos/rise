from django.contrib import admin

from .models import EventoDePoder, Inscrito, Mge, Punido, Ranking

# Register your models here.
admin.site.register(Mge)
admin.site.register(Ranking)
admin.site.register(Punido)
admin.site.register(Inscrito)
admin.site.register(EventoDePoder)
