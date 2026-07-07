from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Embarcacion
from .serializers import EmbarcacionSerializer

class EmbarcacionViewSet(viewsets.ModelViewSet):
    queryset = Embarcacion.objects.filter(activo=True)
    serializer_class = EmbarcacionSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['nombre', 'matricula']
    ordering_fields = ['nombre', 'fecha_registro']
