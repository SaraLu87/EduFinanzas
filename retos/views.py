from rest_framework import status, viewsets
from rest_framework.response import Response
from .serializers import RetoSerializer, RetoCreateUpdateSerializer
from .services import (
    retos_crear, reto_ver, retos_listar,
    retos_actualizar, retos_eliminar
)

class RetoViewSet(viewsets.ViewSet):
    """
    Endpoints:
    - GET    /api/retos/        -> list
    - GET    /api/retos/{id}/   -> retrieve
    - POST   /api/retos/        -> create
    - PUT    /api/retos/{id}/   -> update
    - DELETE /api/retos/{id}/   -> destroy
    """

    def list(self, request):
        """Listar todos los retos"""
        data = retos_listar()
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Obtener un reto por ID"""
        item = reto_ver(int(pk))
        if not item:
            return Response({"detail": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(item, status=status.HTTP_200_OK)

    def create(self, request):
        """Crear un nuevo reto"""
        serializer = RetoCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        nuevo_id = retos_crear(**serializer.validated_data)
        item = reto_ver(nuevo_id)
        return Response(item, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Actualizar un reto existente"""
        serializer = RetoCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        filas = retos_actualizar(int(pk), **serializer.validated_data)
        if filas == 0:
            return Response({"detail": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        item = reto_ver(int(pk))
        return Response(item, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        """Eliminar un reto"""
        filas = retos_eliminar(int(pk))
        if filas == 0:
            return Response({"detail": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
