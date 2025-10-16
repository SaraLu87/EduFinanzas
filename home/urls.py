from django.urls import path
from .views import *

urlpatterns = [
    path('temas/', tema_listar, name='tema_listar'),
    path('temas/crear/', tema_crear, name='tema_crear'),
    path('temas/editar/<int:id>/', tema_editar, name='tema_editar'),
    path('temas/eliminar/<int:id>/', tema_eliminar, name='tema_eliminar'),
]