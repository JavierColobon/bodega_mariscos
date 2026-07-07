from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import RecepcionItem
from .serializers import RecepcionItemSerializer
from faenas.models import Faena

class RecepcionItemViewSet(viewsets.ModelViewSet):
    queryset = RecepcionItem.objects.all()
    serializer_class = RecepcionItemSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['faena', 'especie']
    
    @action(detail=False, methods=['post'])
    def recibir_faena(self, request):
        """
        Recibir múltiples items de captura para una faena
        Espera: {
            "faena_id": 1,
            "receptor_id": 2,
            "items": [
                {"especie": "Pargo", "peso_kg": 50, "precio_unitario": 3.5},
                {"especie": "Corvina", "peso_kg": 30, "precio_unitario": 2.8}
            ]
        }
        """
        faena_id = request.data.get('faena_id')
        receptor_id = request.data.get('receptor_id')
        items = request.data.get('items', [])
        
        try:
            faena = Faena.objects.get(id=faena_id)
        except Faena.DoesNotExist:
            return Response(
                {'error': 'Faena no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if faena.estado != 'EN_CURSO':
            return Response(
                {'error': 'La faena debe estar EN_CURSO para recibirse'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Crear items de recepción
        items_creados = []
        for item_data in items:
            item_data['faena'] = faena.id
            serializer = RecepcionItemSerializer(data=item_data)
            if serializer.is_valid():
                item = serializer.save()
                items_creados.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Actualizar estado de faena
        faena.estado = 'RECIBIDO'
        faena.receptor_id = receptor_id
        from django.utils import timezone
        faena.fecha_entrada_real = timezone.now().date()
        faena.save()
        
        return Response({
            'status': 'Recepción registrada exitosamente',
            'items': items_creados,
            'total_venta': faena.total_venta,
            'deuda_pendiente': faena.deuda_pendiente
        }, status=status.HTTP_201_CREATED)
