from rest_framework import status, viewsets
from rest_framework.response import Response
from .serializers import (
    ProgresoCreateUpdateSerializer,
    ProgresoSerializer
)
from .services import (
    progreso_crear,
    progreso_ver,
    progreso_listar,
    progreso_actualizar,
    progreso_eliminar
)


class ProgresoViewSet(viewsets.ViewSet):
    """
    Endpoints:
    - GET    /api/progresos/        -> list
    - GET    /api/progresos/{id}/   -> retrieve
    - POST   /api/progresos/        -> create
    - PUT    /api/progresos/{id}/   -> update
    - DELETE /api/progresos/{id}/   -> destroy
    """

    def list(self, request):
        """Listar todos los progresos"""
        data = progreso_listar()
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Obtener un progreso por su ID"""
        item = progreso_ver(int(pk))
        if not item:
            return Response({"detail": "Progreso no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(item, status=status.HTTP_200_OK)

    def create(self, request):
        """Crear un nuevo progreso"""
        serializer = ProgresoCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        nuevo_id = progreso_crear(**serializer.validated_data)
        item = progreso_ver(nuevo_id)
        return Response(item, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Actualizar un progreso existente"""
        serializer = ProgresoCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        filas = progreso_actualizar(int(pk), **serializer.validated_data)
        if filas == 0:
            return Response({"detail": "Progreso no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        item = progreso_ver(int(pk))
        return Response(item, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        """Eliminar un progreso"""
        filas = progreso_eliminar(int(pk))
        if filas == 0:
            return Response({"detail": "Progreso no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
