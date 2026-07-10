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
        from django.db.models import Sum
        from faenas.models import Faena
    
        deuda = Faena.objects.filter(
            capitan=self,
            estado__in=['PENDIENTE', 'EN_CURSO', 'RECIBIDO']
        ).aggregate(Sum('deuda_pendiente'))['deuda_pendiente__sum'] or 0
    
        self.deuda_total = deuda
        self.save()
        return self.deuda_total

    def obtener_historial_faenas(self):
        """Retorna todas las faenas del capitán"""
        return self.faenas.all().order_by('-fecha_creacion')

    def obtener_estadisticas(self):
        """Retorna estadísticas del capitán"""
        from django.db.models import Sum, Count
    
    
