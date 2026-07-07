from rest_framework import serializers
from .models import Capitan

class CapitanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Capitan
        fields = ['id', 'nombre', 'documento', 'telefono', 'direccion', 'email', 'deuda_total', 'activo', 'fecha_registro']
