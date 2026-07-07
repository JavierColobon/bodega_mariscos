from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Faena, Gasto
from .serializers import (
    FaenaListSerializer, FaenaDetailSerializer, 
    FaenaCreateUpdateSerializer, GastoSerializer
)

class FaenaViewSet(viewsets.ModelViewSet):
    queryset = Faena.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['estado', 'capitan', 'embarcacion', 'fecha_salida']
    search_fields = ['codigo_faena', 'capitan__nombre', 'embarcacion__nombre']
    ordering_fields = ['fecha_creacion', 'fecha_salida', 'estado']
    ordering = ['-fecha_creacion']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return FaenaListSerializer
        elif self.action == 'retrieve':
            return FaenaDetailSerializer
        else:
            return FaenaCreateUpdateSerializer
    
    @action(detail=True, methods=['post'])
    def agregar_gasto(self, request, pk=None):
        """Agregar un gasto a una faena"""
        faena = self.get_object()
        serializer = GastoSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(faena=faena)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def iniciar_faena(self, request, pk=None):
        """Cambiar estado a EN_CURSO"""
        faena = self.get_object()
        if faena.estado == 'PENDIENTE':
            faena.estado = 'EN_CURSO'
            faena.save()
            return Response({'status': 'Faena iniciada'})
        return Response(
            {'error': 'La faena no está en estado PENDIENTE'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['post'])
    def cerrar_faena(self, request, pk=None):
        """Cerrar una faena completamente"""
        faena = self.get_object()
        if faena.estado == 'RECIBIDO':
            faena.estado = 'CERRADO'
            faena.save()
            # Actualizar deuda del capitán
            faena.capitan.actualizar_deuda_total()
            return Response({'status': 'Faena cerrada exitosamente'})
        return Response(
            {'error': 'La faena debe estar en estado RECIBIDO para cerrarse'},
            status=status.HTTP_400_BAD_REQUEST
        )

class GastoViewSet(viewsets.ModelViewSet):
    queryset = Gasto.objects.all()
    serializer_class = GastoSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['faena', 'tipo']
