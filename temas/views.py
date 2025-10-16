from rest_framework import status, viewsets
from rest_framework.response import Response
from .serializers import (
    TemaCreateUpdateSerializer,
    TemaSerializer
)
from .services import (
    temas_crear, tema_ver, temas_listar,
    temas_actualizar, temas_eliminar
)

class TemaViewSet(viewsets.ViewSet):
    """
    Endpoints:
    - GET    /api/temas/        -> list
    - GET    /api/temas/{id}/   -> retrieve
    - POST   /api/temas/        -> create
    - PUT    /api/temas/{id}/   -> update
    - DELETE /api/temas/{id}/   -> destroy
    """

    def list(self, request):
        """Listar todos los temas"""
        data = temas_listar()
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Obtener un tema por ID"""
        item = tema_ver(int(pk))
        if not item:
            return Response({"detail": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(item, status=status.HTTP_200_OK)

    def create(self, request):
        """Crear un nuevo tema"""
        serializer = TemaCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        nuevo_id = temas_crear(**serializer.validated_data)
        item = tema_ver(nuevo_id)
        return Response(item, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Actualizar un tema existente"""
        serializer = TemaCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        filas = temas_actualizar(int(pk), **serializer.validated_data)
        if filas == 0:
            return Response({"detail": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        item = tema_ver(int(pk))
        return Response(item, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        """Eliminar un tema"""
        filas = temas_eliminar(int(pk))
        if filas == 0:
            return Response({"detail": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
