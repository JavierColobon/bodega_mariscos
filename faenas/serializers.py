from rest_framework import serializers
from .models import Faena, Gasto
from usuarios.serializers import UsuarioSerializer
from embarcaciones.serializers import EmbarcacionSerializer
from capitanes.serializers import CapitanSerializer

class GastoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gasto
        fields = ['id', 'tipo', 'descripcion', 'monto', 'fecha_registro']

class FaenaListSerializer(serializers.ModelSerializer):
    embarcacion_nombre = serializers.CharField(source='embarcacion.nombre', read_only=True)
    capitan_nombre = serializers.CharField(source='capitan.nombre', read_only=True)
    despachador_nombre = serializers.CharField(source='despachador.get_full_name', read_only=True)
    
    class Meta:
        model = Faena
        fields = [
            'id', 'codigo_faena', 'embarcacion_nombre', 'capitan_nombre', 'despachador_nombre',
            'fecha_salida', 'fecha_entrada_est', 'fecha_entrada_real', 'estado',
            'total_gastos', 'total_venta', 'deuda_pendiente', 'fecha_creacion'
        ]

class FaenaDetailSerializer(serializers.ModelSerializer):
    embarcacion = EmbarcacionSerializer(read_only=True)
    capitan = CapitanSerializer(read_only=True)
    despachador = UsuarioSerializer(read_only=True)
    receptor = UsuarioSerializer(read_only=True)
    gastos = GastoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Faena
        fields = [
            'id', 'codigo_faena', 'embarcacion', 'capitan', 'despachador', 'receptor',
            'fecha_salida', 'fecha_entrada_est', 'fecha_entrada_real', 'estado',
            'total_gastos', 'total_venta', 'deuda_inicial', 'deuda_descontada',
            'deuda_pendiente', 'saldo_favor_capitan', 'gastos', 'notas',
            'fecha_creacion', 'fecha_actualizacion'
        ]

class FaenaCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faena
        fields = [
            'embarcacion', 'capitan', 'despachador', 'receptor',
            'fecha_salida', 'fecha_entrada_est', 'fecha_entrada_real',
            'estado', 'deuda_descontada', 'notas'
        ]
