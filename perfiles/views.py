from rest_framework import status, viewsets
from rest_framework.response import Response
from .serializers import (
    PerfilCreateUpdateSerializer,
    PerfilSerializer
)
from .services import (
    perfil_crear, perfil_ver, perfil_listar,
    perfil_actualizar, perfil_eliminar
)


class PerfilViewSet(viewsets.ViewSet):
    """
    Endpoints:
    - GET    /api/perfiles/        -> list
    - GET    /api/perfiles/{id}/   -> retrieve
    - POST   /api/perfiles/        -> create
    - PUT    /api/perfiles/{id}/   -> update
    - DELETE /api/perfiles/{id}/   -> destroy
    """

    def list(self, request):
        """Listar todos los perfiles"""
        data = perfil_listar()
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Obtener un perfil por ID"""
        item = perfil_ver(int(pk))
        if not item:
            return Response({"detail": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(item, status=status.HTTP_200_OK)

    def create(self, request):
        """Crear un nuevo perfil"""
        serializer = PerfilCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        nuevo_id = perfil_crear(**serializer.validated_data)
        item = perfil_ver(nuevo_id)
        return Response(item, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Actualizar un perfil existente"""
        serializer = PerfilCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        filas = perfil_actualizar(int(pk), **serializer.validated_data)
        if filas == 0:
            return Response({"detail": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        item = perfil_ver(int(pk))
        return Response(item, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        """Eliminar un perfil"""
        filas = perfil_eliminar(int(pk))
        if filas == 0:
            return Response({"detail": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
