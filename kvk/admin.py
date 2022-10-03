from django.contrib import admin

from .models import Kvk, Zerado, AdicionalDeFarms, Etapas, PontosDeMGE

# Register your models here.

admin.site.register(Kvk)
admin.site.register(Zerado)
admin.site.register(AdicionalDeFarms)
admin.site.register(PontosDeMGE)
admin.site.register(Etapas)
