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
    
    # def get_permissions(self):
    #     """
    #     Retorna los permisos dinámicamente según la acción.
    #     """
    #     if self.action == "list":  # Solo para el método list
    #         permission_classes = [permisosAdministrador]
    #     else:
    #         permission_classes = self.permission_classes
    #     return [perm() for perm in permission_classes]
    
    
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
        from django.db import IntegrityError as DjangoIntegrityError
        try:
            filas = usuarios_eliminar(int(pk))
            if filas == 0:
                return Response({"detail": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except DjangoIntegrityError as e:
            # Error de integridad referencial (foreign key constraint)
            return Response(
                {"detail": "No se puede eliminar este usuario porque tiene datos relacionados (perfiles, tips, progreso). Primero elimina los registros dependientes."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            # Otros errores
            return Response(
                {"detail": f"Error al eliminar usuario: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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


# Clase para el registro de usuarios (usuario + perfil)
class RegistroView(APIView):
    """
    Endpoint para registrar un nuevo usuario con su perfil.
    Proceso en dos pasos:
    1. Crea el usuario con correo, contraseña y rol='Usuario'
    2. Crea el perfil asociado con nombre, edad y foto opcional
    """
    def post(self, request):
        # Extraer datos del usuario
        correo = request.data.get("correo")
        contrasena = request.data.get("contrasena")

        # Extraer datos del perfil
        nombre_perfil = request.data.get("nombre_perfil")
        edad = request.data.get("edad")
        foto_perfil = request.data.get("foto_perfil", "perfiles/default.png")

        # Validar que los campos requeridos están presentes
        if not correo or not contrasena:
            return Response(
                {"detail": "El correo y la contraseña son obligatorios"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not nombre_perfil or not edad:
            return Response(
                {"detail": "El nombre del perfil y la edad son obligatorios"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Paso 1: Crear usuario con rol 'Usuario'
            from .services import usuarios_crear
            id_usuario = usuarios_crear(
                correo=correo,
                contrasena=contrasena,
                rol='Usuario'
            )

            if not id_usuario:
                return Response(
                    {"detail": "Error al crear el usuario"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Paso 2: Crear perfil asociado
            from perfiles.services import perfil_crear
            id_perfil = perfil_crear(
                id_usuario=id_usuario,
                nombre_perfil=nombre_perfil,
                edad=int(edad),
                foto_perfil=foto_perfil
            )

            if not id_perfil:
                # Si falla la creación del perfil, idealmente deberíamos hacer rollback del usuario
                # pero por ahora simplemente retornamos error
                return Response(
                    {"detail": "Error al crear el perfil"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Obtener datos completos del usuario creado
            from .services import usuario_ver
            usuario = usuario_ver(id_usuario)

            # Obtener datos del perfil creado
            from perfiles.services import perfil_ver
            perfil = perfil_ver(id_perfil)

            # Retornar respuesta exitosa con los datos
            return Response(
                {
                    "message": "Usuario registrado exitosamente",
                    "usuario": usuario,
                    "perfil": perfil
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            # Capturar cualquier error y devolverlo
            return Response(
                {"detail": f"Error en el registro: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


