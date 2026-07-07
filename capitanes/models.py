from django.db import models

class Capitan(models.Model):
    """
    Modelo para los capitanes de embarcaciones
    """
    nombre = models.CharField(max_length=100)
    documento = models.CharField(max_length=50, unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    deuda_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Capitán'
        verbose_name_plural = 'Capitanes'
        ordering = ['nombre']
        
    def __str__(self):
        return self.nombre
    
    def actualizar_deuda_total(self):
        """Recalcula la deuda total del capitán basado en faenas pendientes"""
        
