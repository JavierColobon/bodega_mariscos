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
    inlines = [GastoInline]
    list_filter = ['estado', 'fecha_salida', 'embarcacion']
    search_fields = ['codigo_faena', 'capitan__nombre', 'embarcacion__nombre']
    readonly_fields = [
        'codigo_faena', 'total_gastos', 'total_venta', 
        'deuda_inicial', 'deuda_pendiente', 'saldo_favor_capitan',
        'fecha_creacion', 'fecha_actualizacion'
    ]
    
    fieldsets = (
        ('Información General', {
            'fields': ('codigo_faena', 'embarcacion', 'capitan', 'despachador', 'receptor')
        }),
        ('Fechas', {
            'fields': ('fecha_salida', 'fecha_entrada_est')
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
    list_display = ['faena', 'tipo', 'monto', 'fecha_registro']
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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Si estamos en la vista de detalle filtrada, aplicamos el filtro por faena_id guardado en el request
        if getattr(request, 'show_gasto_details', False):
            faena_id = getattr(request, 'gasto_faena_id', None)
            if faena_id:
                qs = qs.filter(faena_id=faena_id)
        return qs

    def changelist_view(self, request, extra_context=None):
        from django.db.models import Sum, Min

        # Comprobar si se solicitó la vista de detalle
        show_details = 'detail' in request.GET

        if show_details:
            # Hacemos una copia mutable de GET para quitar los parámetros que confunden a Django Admin
            q_dict = request.GET.copy()
            faena_id = q_dict.get('faena_id')
            q_dict.pop('faena_id', None)
            q_dict.pop('detail', None)
            request.GET = q_dict

            # Guardamos los parámetros de filtrado en el request para usarlos en get_queryset
            request.show_gasto_details = True
            request.gasto_faena_id = faena_id

            extra_context = extra_context or {}
            extra_context['show_details'] = True
            return super().changelist_view(request, extra_context=extra_context)

        response = super().changelist_view(request, extra_context=extra_context)

        try:
            # Obtener el queryset filtrado por la vista de administración
            qs = response.context_data['cl'].queryset

            # Agrupar por faena y obtener el monto total y la fecha del primer registro de gasto
            resumen = (
                qs.values('faena__id', 'faena__codigo_faena')
                .annotate(total_monto=Sum('monto'), fecha=Min('fecha_registro'))
                .order_by('-fecha')
            )

            # Calcular el total general de los gastos filtrados
            total_general = qs.aggregate(total=Sum('monto'))['total'] or 0

            # Añadir los datos al contexto de la plantilla
            response.context_data['resumen_gastos'] = resumen
            response.context_data['total_general'] = total_general
            response.context_data['show_details'] = False
        except Exception as e:
            import traceback
            traceback.print_exc()

        return response

