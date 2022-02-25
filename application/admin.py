from django.contrib import admin
from .models import People


class PeopleAdmin(admin.ModelAdmin):
    list_display =('name', 'level', 'number')


admin.site.register(People, PeopleAdmin)
