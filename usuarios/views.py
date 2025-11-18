from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import permisosAdministrador, permisosUsuarios
from .serializers import (
    UsuarioCreateUpdateSerializer,
    UsuarioSerializer
)
from .services import (
    usuarios_crear, usuario_ver, usuarios_listar,
    usuarios_actualizar, usuarios_eliminar, login_usuario
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
    permission_classes = [permisosUsuarios]
    
    def get_permissions(self):
        """
        Retorna los permisos dinámicamente según la acción.
        """
        if self.action == "list":  # Solo para el método list
            permission_classes = [permisosAdministrador]
        else:
            permission_classes = self.permission_classes
        return [perm() for perm in permission_classes]
    
    
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
        nuevo_id = usuarios_crear(**serializer.validated_data)
        #nuevo_id = nuevo["usuario"]["id_usuario"]
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

# Clase para el logeo del usuario class LoginView(APIView):
class LoginView(APIView):
    def post(self, request):
        correo = request.data.get("correo")
        contrasena = request.data.get("contrasena")

        resultado = login_usuario(correo, contrasena)

        if resultado is None:
            return Response({"detail": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        if resultado is False:
            return Response({"detail": "Contraseña incorrecta"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(resultado, status=status.HTTP_200_OK)


