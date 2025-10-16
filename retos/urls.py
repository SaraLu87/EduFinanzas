from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_retos import RetoViewSet
from .views import TemaViewSet  # ya existente

router = DefaultRouter()
router.register(r'temas', TemaViewSet, basename='temas')
router.register(r'retos', RetoViewSet, basename='retos')

urlpatterns = [
    path('api/', include(router.urls)),
]
