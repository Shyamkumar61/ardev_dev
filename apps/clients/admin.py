from django.contrib import admin
from apps.clients.models import Client

# Register your models here.


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):

    search_fields = ['service', 'designation']
    autocomplete_fields = ['service', 'designation']
