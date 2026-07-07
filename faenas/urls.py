from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FaenaViewSet, GastoViewSet

router = DefaultRouter()
router.register(r'', FaenaViewSet, basename='faena')
router.register(r'gastos', GastoViewSet, basename='gasto')

urlpatterns = [
    path('', include(router.urls)),
]
