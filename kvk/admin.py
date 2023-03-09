from django.contrib import admin

from .models import AdicionalDeFarms, Cargo, Etapas, Kvk, PontosDeMGE, Zerado

# Register your models here.

admin.site.register(Kvk)
admin.site.register(Zerado)
admin.site.register(AdicionalDeFarms)
admin.site.register(PontosDeMGE)
admin.site.register(Etapas)
admin.site.register(Cargo)
