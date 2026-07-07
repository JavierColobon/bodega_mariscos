from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PrecioEspecieViewSet

router = DefaultRouter()
router.register(r'especies', PrecioEspecieViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
