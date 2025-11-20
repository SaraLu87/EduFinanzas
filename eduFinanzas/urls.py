"""
URL configuration for eduFinanzas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from temas.views import TemaViewSet
from usuarios.views import UsuarioViewSet, LoginView, RegisterView
from perfiles.views import PerfilViewSet
from retos.views import RetoViewSet
from tips.views import TipPeriodicaViewSet
from progresos.views import ProgresoViewSet
from solucionarReto.views import SolucionRetoView
from django.conf import settings
from django.conf.urls.static import static


# Crear el router y registrar el ViewSet
router = DefaultRouter()
router.register(r'temas', TemaViewSet, basename='temas')
router.register(r'usuarios', UsuarioViewSet, basename='usuarios')
router.register(r'perfiles', PerfilViewSet, basename='perfiles')
router.register(r'retos', RetoViewSet, basename='retos')
router.register(r'tips', TipPeriodicaViewSet, basename='tips')
router.register(r'progresos', ProgresoViewSet, basename='progresos')

# Definir las rutas principales
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/solucionar_reto/', SolucionRetoView.as_view(), name='solucionar_reto'),
    path('api/login_usuario/', LoginView.as_view(), name='login_usuario'),
    path('api/register/', RegisterView.as_view(), name='register'),  # Endpoint de registro público
]

# ============================================================================
# CONFIGURACIÓN PARA SERVIR ARCHIVOS MEDIA (IMÁGENES) EN DESARROLLO
# ============================================================================
# Pillow procesa y guarda las imágenes en MEDIA_ROOT (configurado en settings.py)
# Esta configuración permite acceder a las imágenes a través de MEDIA_URL
#
# Ejemplo de uso:
#   - MEDIA_ROOT = BASE_DIR / 'mediafiles'  (donde se guardan físicamente)
#   - MEDIA_URL = 'media/'                   (URL para acceder)
#   - Imagen guardada en: /mediafiles/perfiles/foto.jpg
#   - URL de acceso: http://localhost:8000/media/perfiles/foto.jpg
#
# Las carpetas donde se guardan las imágenes son:
#   - /mediafiles/perfiles/   → Fotos de perfil de usuarios
#   - /mediafiles/temas/      → Imágenes de temas educativos
#   - /mediafiles/retos/      → Imágenes de retos/desafíos
#
# IMPORTANTE: En producción, usar un servidor web (Nginx/Apache) para servir
# archivos estáticos en lugar de Django, por razones de rendimiento y seguridad.
# ============================================================================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



