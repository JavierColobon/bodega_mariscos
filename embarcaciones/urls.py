from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmbarcacionViewSet

router = DefaultRouter()
router.register(r'', EmbarcacionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
