from django.db import models

class PrecioEspecie(models.Model):
    """
    Modelo para configurar precios por especie
    """
    UNIDADES = (
        ('libra', 'Por Libra'),
        ('kg', 'Por Kilogramo'),
        ('unidad', 'Por Unidad'),
    )
    
    especie = models.CharField(max_length=100, unique=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    unidad_medida = models.CharField(max_length=10, choices=UNIDADES, default='libra')
    vigente_desde = models.DateField()
    vigente_hasta = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Precio de Especie'
        verbose_name_plural = 'Precios de Especies'
        ordering = ['especie']
        
    def __str__(self):
        return f"{self.especie} - ${self.precio}/{self.get_unidad_medida_display()}"
