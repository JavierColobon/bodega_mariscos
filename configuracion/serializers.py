from rest_framework import serializers
from .models import PrecioEspecie

class PrecioEspecieSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrecioEspecie
        fields = [
            'id', 'especie', 'precio_por_kg', 'vigente_desde',
            'vigente_hasta', 'activo'
        ]
