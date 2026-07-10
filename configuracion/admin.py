from django.contrib import admin
from .models import PrecioEspecie

@admin.register(PrecioEspecie)
class PrecioEspecieAdmin(admin.ModelAdmin):
    list_display = ['especie', 'precio_por_kg', 'vigente_desde', 'vigente_hasta', 'activo']
    list_filter = ['activo', 'vigente_desde']
    search_fields = ['especie']
    ordering = ['especie']
