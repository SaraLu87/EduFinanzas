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
    - GET    /api/usuarios/        -> list (requiere rol Admin)
    - GET    /api/usuarios/{id}/   -> retrieve (requiere autenticación)
    - POST   /api/usuarios/        -> create (PÚBLICO - para registro)
    - PUT    /api/usuarios/{id}/   -> update (requiere autenticación)
    - DELETE /api/usuarios/{id}/   -> destroy (requiere autenticación)
    """
    # Permisos por defecto para métodos autenticados
    permission_classes = [permisosUsuarios]

    def get_permissions(self):
        """
        Retorna los permisos dinámicamente según la acción.
        - create (POST): Público, permite registro sin autenticación
        - list (GET /usuarios/): Solo administradores
        - Otros métodos: Requieren autenticación
        """
        if self.action == "create":
            # Permitir registro público (sin autenticación)
            return []
        elif self.action == "list":
            # Solo administradores pueden listar todos los usuarios
            return [permisosAdministrador()]
        else:
            # Otros métodos requieren autenticación
            return [permisosUsuarios()]
    
    
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

# ============================================================================
# CLASE DE LOGIN - Autenticación de usuarios
# ============================================================================
class LoginView(APIView):
    """
    Vista para iniciar sesión
    Endpoint: POST /api/login_usuario/
    No requiere autenticación (público)
    """
    def post(self, request):
        correo = request.data.get("correo")
        contrasena = request.data.get("contrasena")

        resultado = login_usuario(correo, contrasena)

        if resultado is None:
            return Response({"detail": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        if resultado is False:
            return Response({"detail": "Contraseña incorrecta"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(resultado, status=status.HTTP_200_OK)


# ============================================================================
# CLASE DE REGISTRO - Creación de usuario + perfil en una transacción
# ============================================================================
class RegisterView(APIView):
    """
    Vista para registro de nuevos usuarios
    Endpoint: POST /api/register/

    Crea un usuario y su perfil asociado en una sola operación
    No requiere autenticación (público)

    Datos esperados:
    {
        "correo": "usuario@ejemplo.com",
        "contrasena": "ContraseñaSegura123!",
        "rol": "Usuario",
        "perfil": {
            "nombre_perfil": "Juan Pérez",
            "edad": 16
        }
    }
    """
    def post(self, request):
        try:
            # Extraer datos del request
            correo = request.data.get("correo")
            contrasena = request.data.get("contrasena")
            rol = request.data.get("rol", "Usuario")
            perfil_data = request.data.get("perfil", {})

            # Validar datos requeridos
            if not correo or not contrasena:
                return Response(
                    {"detail": "Correo y contraseña son requeridos"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not perfil_data.get("nombre_perfil") or not perfil_data.get("edad"):
                return Response(
                    {"detail": "Nombre y edad del perfil son requeridos"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Paso 1: Crear usuario
            from perfiles.services import perfil_crear, perfil_ver

            try:
                nuevo_usuario_id = usuarios_crear(
                    correo=correo,
                    contrasena=contrasena,
                    rol=rol
                )
            except Exception as e:
                if "correo" in str(e).lower() or "duplicate" in str(e).lower():
                    return Response(
                        {"detail": "Este correo electrónico ya está registrado"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(
                    {"detail": f"Error al crear usuario: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Paso 2: Crear perfil asociado al usuario
            try:
                nuevo_perfil_id = perfil_crear(
                    id_usuario=nuevo_usuario_id,
                    nombre_perfil=perfil_data.get("nombre_perfil"),
                    edad=int(perfil_data.get("edad")),
                    foto_perfil="perfiles/default.png"
                )
            except Exception as e:
                return Response(
                    {"detail": f"Usuario creado pero error al crear perfil: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Paso 3: Obtener datos completos
            usuario_creado = usuario_ver(nuevo_usuario_id)
            perfil_creado = perfil_ver(nuevo_perfil_id)

            # Retornar respuesta exitosa
            return Response(
                {
                    "message": "Registro exitoso",
                    "usuario": usuario_creado,
                    "perfil": perfil_creado
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"detail": f"Error inesperado: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


