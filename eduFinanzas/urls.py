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
from usuarios.views import UsuarioViewSet, LoginView, RegistroView
from perfiles.views import PerfilViewSet
from perfiles.views_usuario import PerfilMeView, PerfilMeUpdateView, ProgresoMeView, ProgresoTemasView
from retos.views import RetoViewSet
from retos.views_usuario import RetosPorTemaView, IniciarRetoView
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
    path('api/registro/', RegistroView.as_view(), name='registro'),

    # Endpoints para usuarios autenticados
    path('api/perfil/me/', PerfilMeView.as_view(), name='perfil_me'),
    path('api/perfil/me/update/', PerfilMeUpdateView.as_view(), name='perfil_me_update'),
    path('api/perfil/me/progreso/', ProgresoMeView.as_view(), name='progreso_me'),
    path('api/perfil/me/progreso-temas/', ProgresoTemasView.as_view(), name='progreso_temas'),
    path('api/temas/<int:id_tema>/retos/', RetosPorTemaView.as_view(), name='retos_por_tema'),
    path('api/retos/<int:id_reto>/iniciar/', IniciarRetoView.as_view(), name='iniciar_reto'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



