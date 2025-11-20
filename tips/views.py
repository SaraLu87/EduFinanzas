from rest_framework import status, viewsets
from rest_framework.response import Response
from .serializers import (
    TipPeriodicaCreateUpdateSerializer,
    TipPeriodicaSerializer
)
from .services import (
    tip_crear, tip_listar, tip_ver,
    tip_actualizar, tip_eliminar
)


class TipPeriodicaViewSet(viewsets.ViewSet):
    """
    Endpoints:
    - GET    /api/tips/        -> list
    - GET    /api/tips/{id}/   -> retrieve
    - POST   /api/tips/        -> create
    - PUT    /api/tips/{id}/   -> update
    - DELETE /api/tips/{id}/   -> destroy
    """

    def list(self, request):
        """Listar todos los tips periódicos"""
        data = tip_listar()
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Obtener un tip por ID"""
        item = tip_ver(int(pk))
        if not item:
            return Response({"detail": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(item, status=status.HTTP_200_OK)

    def create(self, request):
        """Crear un nuevo tip periódico"""
        serializer = TipPeriodicaCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        nuevo_id = tip_crear(**serializer.validated_data)
        item = tip_ver(nuevo_id)
        return Response(item, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Actualizar un tip existente"""
        serializer = TipPeriodicaCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extraer solo los campos que tip_actualizar acepta (sin id_perfil)
        datos = {k: v for k, v in serializer.validated_data.items() if k != 'id_perfil'}
        filas = tip_actualizar(int(pk), **datos)

        if filas == 0:
            return Response({"detail": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        item = tip_ver(int(pk))
        return Response(item, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        """Eliminar un tip"""
        filas = tip_eliminar(int(pk))
        if filas == 0:
            return Response({"detail": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
