from django.contrib import admin

from config.models import Destaque, SiteConfig

# Register your models here.
admin.site.register(SiteConfig)
admin.site.register(Destaque)
