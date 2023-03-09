from django.contrib import admin

# Register your models here.
from .models import Credito, Donation, Semana


class DonationAdmin(admin.ModelAdmin):
    list_display = ["player", "data_da_doacao", "donated"]
    list_filter = ["donated"]
    ordering = ("data_da_doacao", "player")


admin.site.register(Semana)
admin.site.register(Donation, DonationAdmin)
admin.site.register(Credito)
