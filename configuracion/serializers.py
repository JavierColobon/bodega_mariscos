from rest_framework import serializers
from .models import PrecioEspecie

class PrecioEspecieSerializer(serializers.ModelSerializer):
    unidad_medida_display = serializers.CharField(source='get_unidad_medida_display', read_only=True)
    
    class Meta:
        model = PrecioEspecie
        fields = [
            'id', 'especie', 'precio', 'unidad_medida', 'unidad_medida_display',
            'vigente_desde', 'vigente_hasta', 'activo'
        ]
