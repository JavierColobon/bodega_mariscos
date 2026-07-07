from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    """
    Modelo extendido de usuario con roles
    """
    ROLES = (
        ('despachador', 'Despachador'),
        ('receptor', 'Receptor'),
        ('admin', 'Administrador'),
    )
    
    rol = models.CharField(max_length=20, choices=ROLES, default='despachador')
    telefono = models.CharField(max_length=20, blank=True, null=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_rol_display()})"
