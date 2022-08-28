from django.contrib import admin

from osiris.models import Funcao, Marcha, Time

# Register your models here.
admin.site.register(Marcha)
admin.site.register(Funcao)
admin.site.register(Time)
