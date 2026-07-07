from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Capitan
from .serializers import CapitanSerializer

class CapitanViewSet(viewsets.ModelViewSet):
    queryset = Capitan.objects.filter(activo=True)
    serializer_class = CapitanSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['nombre', 'documento']
    ordering_fields = ['nombre', 'deuda_total']
