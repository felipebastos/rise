from django.contrib import admin

from equipments.models import BuffConjunto, Conjunto, Equipamento

# Register your models here.
admin.site.register(Equipamento)
admin.site.register(Conjunto)
admin.site.register(BuffConjunto)
