from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import PrecioEspecie
from .serializers import PrecioEspecieSerializer

class PrecioEspecieViewSet(viewsets.ModelViewSet):
    queryset = PrecioEspecie.objects.filter(activo=True)
    serializer_class = PrecioEspecieSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['especie']
    ordering_fields = ['especie', 'precio_por_kg']
