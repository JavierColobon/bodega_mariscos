from django.contrib import admin
from .models import Faena, Gasto

class GastoInline(admin.TabularInline):
    model = Gasto
    extra = 1
    readonly_fields = ['fecha_registro']
    fields = ['tipo', 'descripcion', 'monto', 'fecha_registro']

@admin.register(Faena)
class FaenaAdmin(admin.ModelAdmin):
    list_display = [
        'codigo_faena', 'embarcacion', 'capitan', 'estado', 
        'fecha_salida', 'fecha_entrada_est', 'total_gastos', 
        'total_venta', 'deuda_pendiente'
    ]
    list_filter = ['estado', 'fecha_salida', 'embarcacion']
    search_fields = ['codigo_faena', 'capitan__nombre', 'embarcacion__nombre']
    readonly_fields = [
        'codigo_faena', 'total_gastos', 'total_venta', 
        'deuda_inicial', 'deuda_pendiente', 'saldo_favor_capitan',
        'fecha_creacion', 'fecha_actualizacion'
    ]
    inlines = [GastoInline]
    
    fieldsets = (
        ('Información General', {
            'fields': ('codigo_faena', 'embarcacion', 'capitan', 'despachador', 'receptor')
        }),
        ('Fechas', {
            'fields': ('fecha_salida', 'fecha_entrada_est', 'fecha_entrada_real')
        }),
        ('Estado y Finanzas', {
            'fields': (
                'estado', 'total_gastos', 'total_venta', 'deuda_inicial',
                'deuda_descontada', 'deuda_pendiente', 'saldo_favor_capitan'
            )
        }),
        ('Adicional', {
            'fields': ('notas', 'fecha_creacion', 'fecha_actualizacion')
        }),
    )
    
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
        formset.save_m2m()
        # Recalcular totales después de guardar gastos
        if hasattr(form.instance, 'calcular_total_gastos'):
            form.instance.calcular_total_gastos()

@admin.register(Gasto)
class GastoAdmin(admin.ModelAdmin):
    list_display = ['faena', 'tipo', 'monto', 'descripcion', 'fecha_registro']
    list_filter = ['tipo', 'fecha_registro']
    search_fields = ['faena__codigo_faena', 'descripcion']
    readonly_fields = ['fecha_registro']
    
    fieldsets = (
        ('Información del Gasto', {
            'fields': ('faena', 'tipo', 'descripcion', 'monto')
        }),
        ('Registro', {
            'fields': ('fecha_registro',)
        }),
    )
