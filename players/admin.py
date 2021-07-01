from django.contrib import admin

# Register your models here.
from .models import Player, Alliance, PlayerStatus

admin.site.register(Alliance)
admin.site.register(Player)
admin.site.register(PlayerStatus)