from django.contrib import admin
from .models import Embarcacion

@admin.register(Embarcacion)
class EmbarcacionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'matricula', 'capacidad_kg', 'tipo', 'activo', 'fecha_registro']
    list_filter = ['activo', 'tipo']
    search_fields = ['nombre', 'matricula']
    ordering = ['nombre']
