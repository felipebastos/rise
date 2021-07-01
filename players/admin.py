from django.contrib import admin

# Register your models here.
from .models import Player, Alliance, PlayerStatus

class PlayerAdmin(admin.ModelAdmin):
    list_display = ['nick', 'game_id', 'rank', 'status']
    search_fields = ['game_id', 'nick']

    # define filter columns list, then a filter widget will be shown at right side of Department list page.
    list_filter = ['rank', 'status']
    # define which field will be pre populated.
    prepopulated_fields = {'game_id': ('game_id',)}
    # define model data list ordering.
    ordering = ('game_id','nick', 'status')


class PlayerStatusAdmin(admin.ModelAdmin):
    list_display = ['player', 'data', 'power', 'killpoints', 'deaths']

    ordering = ('player', 'data', 'power', 'killpoints', 'deaths')


admin.site.register(Alliance)
admin.site.register(Player, PlayerAdmin)
admin.site.register(PlayerStatus, PlayerStatusAdmin)
