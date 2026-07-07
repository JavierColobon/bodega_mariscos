from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecepcionItemViewSet

router = DefaultRouter()
router.register(r'', RecepcionItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
