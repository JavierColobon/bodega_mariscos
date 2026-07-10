from django.contrib import admin
from .models import RecepcionItem

@admin.register(RecepcionItem)
class RecepcionItemAdmin(admin.ModelAdmin):
    list_display = [
        'faena', 'especie', 'peso_kg', 'cantidad', 
        'unidad_medida', 'precio_unitario', 'subtotal', 'fecha_registro'
    ]
    list_filter = ['especie', 'unidad_medida', 'fecha_registro']
    search_fields = ['faena__codigo_faena', 'especie']
    readonly_fields = ['subtotal', 'fecha_registro']
