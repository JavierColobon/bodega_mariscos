from django.contrib import admin
from .models import RecepcionItem, Recepcion

class RecepcionItemInline(admin.TabularInline):
    model = RecepcionItem
    extra = 1
    readonly_fields = ['subtotal', 'fecha_registro']
    fields = ['especie', 'peso_kg', 'cantidad', 'unidad_medida', 'precio_unitario', 'subtotal', 'fecha_registro']

@admin.register(Recepcion)
class RecepcionAdmin(admin.ModelAdmin):
    list_display = ['codigo_faena', 'embarcacion', 'capitan', 'estado', 'fecha_entrada_real', 'total_venta']
    list_filter = ['estado', 'fecha_entrada_real', 'embarcacion']
    search_fields = ['codigo_faena', 'embarcacion__nombre', 'capitan__nombre']
    readonly_fields = ['codigo_faena', 'total_gastos', 'total_venta', 'deuda_inicial', 'deuda_pendiente', 'saldo_favor_capitan']
    inlines = [RecepcionItemInline]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(estado__in=['EN_CURSO', 'RECIBIDO', 'CERRADO'])
