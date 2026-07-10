from django.contrib import admin
from .models import PrecioEspecie

@admin.register(PrecioEspecie)
class PrecioEspecieAdmin(admin.ModelAdmin):
    list_display = ['especie', 'precio', 'unidad_medida', 'vigente_desde', 'vigente_hasta', 'activo']
    list_filter = ['activo', 'unidad_medida', 'vigente_desde']
    search_fields = ['especie']
    ordering = ['especie']
    
    fieldsets = (
        ('Información de la Especie', {
            'fields': ('especie', 'precio', 'unidad_medida')
        }),
        ('Vigencia', {
            'fields': ('vigente_desde', 'vigente_hasta', 'activo')
        }),
    )
