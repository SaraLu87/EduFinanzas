from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .serializers import (
    TemaCreateUpdateSerializer,
    TemaSerializer
)
from .services import (
    temas_crear, tema_ver, temas_listar,
    temas_actualizar, temas_eliminar
)
import os

class TemaViewSet(viewsets.ViewSet):
    """
    ViewSet para gestión de Temas

    Endpoints:
    - GET    /api/temas/        -> list (Listar todos los temas)
    - GET    /api/temas/{id}/   -> retrieve (Obtener un tema por ID)
    - POST   /api/temas/        -> create (Crear nuevo tema con imagen)
    - PUT    /api/temas/{id}/   -> update (Actualizar tema con/sin imagen)
    - DELETE /api/temas/{id}/   -> destroy (Eliminar tema)

    Manejo de imágenes con Pillow:
    - Las imágenes se reciben como archivos multipart/form-data
    - Se procesan con Pillow y se guardan en MEDIA_ROOT/temas/
    - La ruta se almacena en BD como 'temas/nombre_archivo.extension'
    - Para acceder: http://localhost:8000/media/temas/nombre_archivo.extension
    """
    # Configurar parsers para aceptar archivos multipart y JSON
    parser_classes = [MultiPartParser, FormParser, JSONParser]

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
        """
        Crear un nuevo tema con imagen opcional

        Proceso:
        1. Validar datos del formulario con serializer
        2. Si hay imagen, guardarla en /mediafiles/temas/ usando Pillow
        3. Guardar ruta de imagen en BD (ej: 'temas/imagen.jpg')
        4. Crear tema en BD mediante procedimiento almacenado
        5. Retornar tema creado con su ID y ruta de imagen
        """
        serializer = TemaCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data.copy()
        img_file = data.get("img_temas")  # Obtener archivo de imagen del request

        # ===== MANEJO DE IMAGEN CON PILLOW =====
        # Si se envió una imagen, guardarla en el sistema de archivos
        if img_file:
            # Construir ruta relativa para guardar: temas/nombre_archivo.extension
            img_path = f"temas/{img_file.name}"
            # Guardar físicamente el archivo en MEDIA_ROOT/temas/
            # Pillow procesará la imagen automáticamente al guardar
            saved_path = default_storage.save(img_path, ContentFile(img_file.read()))
            # Usar la ruta guardada (Django puede modificar el nombre si ya existe)
            data["img_temas"] = saved_path
        else:
            # Si no hay imagen, usar la imagen por defecto
            data["img_temas"] = "temas/default.png"

        # Crear tema en BD con la ruta de la imagen
        nuevo_id = temas_crear(**data)
        item = tema_ver(nuevo_id)
        return Response(item, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """
        Actualizar un tema existente con o sin nueva imagen

        Proceso:
        1. Validar datos recibidos
        2. Si hay nueva imagen, guardarla con Pillow y actualizar ruta
        3. Si NO hay nueva imagen, mantener la imagen existente
        4. Actualizar tema en BD
        5. Retornar tema actualizado
        """
        serializer = TemaCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data.copy()
        img_file = data.get("img_temas")

        # ===== MANEJO DE IMAGEN AL ACTUALIZAR =====
        if img_file:
            # Si se envió nueva imagen, guardarla con Pillow
            img_path = f"temas/{img_file.name}"
            saved_path = default_storage.save(img_path, ContentFile(img_file.read()))
            data["img_temas"] = saved_path
        else:
            # Si NO se envió imagen, mantener la existente
            tema_actual = tema_ver(int(pk))
            if tema_actual:
                data["img_temas"] = tema_actual.get("img_temas", "temas/default.png")
            else:
                data["img_temas"] = "temas/default.png"

        # Actualizar tema en BD
        filas = temas_actualizar(int(pk), **data)
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
