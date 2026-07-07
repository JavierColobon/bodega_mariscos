from rest_framework import serializers
from .models import Embarcacion

class EmbarcacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Embarcacion
        fields = ['id', 'nombre', 'matricula', 'capacidad_kg', 'tipo', 'activo', 'fecha_registro', 'notas']
