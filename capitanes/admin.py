from django.contrib import admin
from .models import Capitan

@admin.register(Capitan)
class CapitanAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'documento', 'telefono', 'deuda_total', 'activo', 'fecha_registro']
    list_filter = ['activo']
    search_fields = ['nombre', 'documento', 'telefono']
    readonly_fields = ['deuda_total', 'fecha_registro']
    ordering = ['nombre']
