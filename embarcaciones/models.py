from django.db import models

class Embarcacion(models.Model):
    """
    Modelo para las embarcaciones pesqueras
    """
    nombre = models.CharField(max_length=100, unique=True)
    matricula = models.CharField(max_length=50, unique=True, blank=True, null=True)
    capacidad_kg = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tipo = models.CharField(max_length=50, blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateField(auto_now_add=True)
    notas = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Embarcación'
        verbose_name_plural = 'Embarcaciones'
        ordering = ['nombre']
        
    def __str__(self):
        return self.nombre

