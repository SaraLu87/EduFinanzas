from rest_framework import status, viewsets
from rest_framework.response import Response
from .serializers import (
    UsuarioCreateUpdateSerializer,
    UsuarioSerializer
)
from .services import (
    usuarios_crear, usuario_ver, usuarios_listar,
    usuarios_actualizar, usuarios_eliminar
)

class UsuarioViewSet(viewsets.ViewSet):
    """
    Endpoints:
    - GET    /api/usuarios/        -> list
    - GET    /api/usuarios/{id}/   -> retrieve
    - POST   /api/usuarios/        -> create
    - PUT    /api/usuarios/{id}/   -> update
    - DELETE /api/usuarios/{id}/   -> destroy
    """

    def list(self, request):
        data = usuarios_listar()
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        item = usuario_ver(int(pk))
        if not item:
            return Response({"detail": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(item, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = UsuarioCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        nuevo = usuarios_crear(**serializer.validated_data)
        nuevo_id = nuevo["usuario"]["id_usuario"]
        item = usuario_ver(nuevo_id)
        return Response(item, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        serializer = UsuarioCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        filas = usuarios_actualizar(int(pk), **serializer.validated_data)
        if filas == 0:
            return Response({"detail": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        item = usuario_ver(int(pk))
        return Response(item, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        filas = usuarios_eliminar(int(pk))
        if filas == 0:
            return Response({"detail": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

# Create your views here.
