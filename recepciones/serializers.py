from rest_framework import serializers
from .models import RecepcionItem

class RecepcionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecepcionItem
        fields = [
            'id', 'faena', 'especie', 'peso_kg', 'cantidad',
            'unidad_medida', 'precio_unitario', 'subtotal', 'fecha_registro'
        ]
    
    def create(self, validated_data):
        item = RecepcionItem.objects.create(**validated_data)
        # Calcular subtotal
        if item.unidad_medida == 'kg':
            item.subtotal = item.peso_kg * item.precio_unitario
        else:
            item.subtotal = item.cantidad * item.precio_unitario
        item.save()
        # Actualizar total_venta de la faena
        item.faena.calcular_total_venta()
        return item
