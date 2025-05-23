from django.contrib import admin
from rangefilter.filters import (
    DateRangeQuickSelectListFilterBuilder,
)

# Register your models here.
from .models import Advertencia, Alliance, Player, PlayerStatus


class PlayerAdmin(admin.ModelAdmin):
    list_display = ["nick", "game_id", "specialty", "status"]
    search_fields = ["nick", "game_id"]

    # define filter columns list, then a filter widget will be
    # shown at right side of Department list page.
    list_filter = ["rank", "status", "specialty"]
    # define which field will be pre populated.
    prepopulated_fields = {"game_id": ("game_id",)}
    # define model data list ordering.
    ordering = ("nick", "game_id", "status")


class PlayerStatusAdmin(admin.ModelAdmin):
    list_display = [
        "player",
        "data",
        "power",
        "killpoints",
        "deaths",
        "killst4",
        "killst5",
    ]

    ordering = ("player", "data", "power", "killpoints", "deaths")
    search_fields = ["player__nick", "player__game_id"]

    list_filter = (("data", DateRangeQuickSelectListFilterBuilder()),)


admin.site.register(Alliance)
admin.site.register(Player, PlayerAdmin)
admin.site.register(PlayerStatus, PlayerStatusAdmin)
admin.site.register(Advertencia)
