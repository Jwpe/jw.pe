from django.contrib import admin
from projects.models import Pun


class PunAdmin(admin.ModelAdmin):
    list_display  = ('pun_target', 'text', 'url')
    search_fields = ('pun_target', 'text')

admin.site.register(Pun, PunAdmin)
