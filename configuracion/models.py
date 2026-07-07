from django.db import models

class PrecioEspecie(models.Model):
    """
    Modelo para configurar precios por especie
    """
    especie = models.CharField(max_length=100, unique=True)
    precio_por_kg = models.DecimalField(max_digits=10, decimal_places=2)
    vigente_desde = models.DateField()
    vigente_hasta = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Precio de Especie'
        verbose_name_plural = 'Precios de Especies'
        ordering = ['especie']
        
    def __str__(self):
        return f"{self.especie} - ${self.precio_por_kg}/kg"

