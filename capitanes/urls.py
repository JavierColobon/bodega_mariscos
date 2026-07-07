from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CapitanViewSet

router = DefaultRouter()
router.register(r'', CapitanViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
