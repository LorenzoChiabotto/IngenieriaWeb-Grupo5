from django.contrib import admin
from catalog.models import Home
from .models import Usuario
admin.site.register(Usuario)

class AdmiPrueba(admin.ModelAdmin):
    search_fields = ('titulo','texto')
admin.site.register(Home, AdmiPrueba)
# Register your models here.
