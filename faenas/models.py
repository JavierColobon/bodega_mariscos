from django.db import models
from django.utils import timezone
from embarcaciones.models import Embarcacion
from capitanes.models import Capitan
from usuarios.models import Usuario

class Faena(models.Model):
    """
    Modelo principal para el registro de faenas/despachos
    """
    ESTADOS = (
        ('PENDIENTE', 'Pendiente'),
        ('EN_CURSO', 'En Curso'),
        ('RECIBIDO', 'Recibido'),
        ('CERRADO', 'Cerrado'),
        ('CANCELADO', 'Cancelado'),
    )
    
    codigo_faena = models.CharField(max_length=50, unique=True, editable=False)
    embarcacion = models.ForeignKey(Embarcacion, on_delete=models.PROTECT, related_name='faenas')
    capitan = models.ForeignKey(Capitan, on_delete=models.PROTECT, related_name='faenas')
    despachador = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='faenas_despachadas')
    receptor = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='faenas_recibidas', null=True, blank=True)
    
    fecha_salida = models.DateField()
    fecha_entrada_est = models.DateField()
    fecha_entrada_real = models.DateField(null=True, blank=True)
    
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    
    total_gastos = models.DecimalField(max_digits=12, decimal_places=2, default=0, editable=False)
    total_venta = models.DecimalField(max_digits=12, decimal_places=2, default=0, editable=False)
    deuda_inicial = models.DecimalField(max_digits=12, decimal_places=2, default=0, editable=False)
    deuda_descontada = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deuda_pendiente = models.DecimalField(max_digits=12, decimal_places=2, default=0, editable=False)
    saldo_favor_capitan = models.DecimalField(max_digits=12, decimal_places=2, default=0, editable=False)
    
    notas = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Faena'
        verbose_name_plural = 'Faenas'
        ordering = ['-fecha_creacion']
        
    def __str__(self):
        return f"{self.codigo_faena} - {self.embarcacion.nombre}"
    
    def save(self, *args, **kwargs):
        if not self.codigo_faena:
            # Generar código automático FAE-YYYYMMDD-001
            fecha = timezone.now().strftime('%Y%m%d')
            ultimo = Faena.objects.filter(codigo_faena__startswith=f'FAE-{fecha}').count()
            self.codigo_faena = f'FAE-{fecha}-{str(ultimo + 1).zfill(3)}'
        
        # Calcular deuda inicial igual a total gastos
        self.deuda_inicial = self.total_gastos
        
        # Calcular deuda pendiente
        self.deuda_pendiente = self.deuda_inicial - self.deuda_descontada
        
        # Calcular saldo a favor del capitán
        if self.total_venta > self.deuda_inicial:
            self.saldo_favor_capitan = self.total_venta - self.deuda_

class Gasto(models.Model):
    """
    Modelo para registrar gastos de cada faena
    """
    TIPOS_GASTO = (
        ('gasolina', 'Gasolina'),
        ('hielo', 'Hielo'),
        ('carnada', 'Carnada'),
        ('viveres', 'Víveres'),
        ('material', 'Material de Pesca'),
        ('otros', 'Otros'),
    )
    
    faena = models.ForeignKey(Faena, on_delete=models.CASCADE, related_name='gastos')
    tipo = models.CharField(max_length=20, choices=TIPOS_GASTO)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Gasto'
        verbose_name_plural = 'Gastos'
        ordering = ['tipo']
        
    def __str__(self):
        return f"{self.get_tipo_display()} - ${self.monto}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Actualizar total_gastos de la faena
        self.faena.calcular_total_gastos()
