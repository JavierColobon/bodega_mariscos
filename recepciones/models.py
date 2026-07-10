from django.db import models
from faenas.models import Faena
from configuracion.models import PrecioEspecie

class RecepcionItem(models.Model):
    """
    Modelo para registrar especies recibidas en cada faena
    """
    UNIDADES = (
        ('kg', 'Kilogramos'),
        ('unidad', 'Unidades'),
        ('libra', 'Libras'),
    )
    
    faena = models.ForeignKey(Faena, on_delete=models.CASCADE, related_name='recepciones')
    especie = models.CharField(max_length=100)
    peso_kg = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cantidad = models.IntegerField(default=0, help_text="Cantidad en unidades")
    unidad_medida = models.CharField(max_length=10, choices=UNIDADES, default='kg')
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Item de Recepción'
        verbose_name_plural = 'Items de Recepción'

    def save(self, *args, **kwargs):
        """Calcular subtotal automáticamente"""
        if self.unidad_medida == 'kg':
            self.subtotal = self.peso_kg * self.precio_unitario
        else:
            self.subtotal = self.cantidad * self.precio_unitario
    
        super().save(*args, **kwargs)
    
    # Actualizar total_venta de la faena
        self.faena.calcular_total_venta()

