from rest_framework.permissions import BasePermission


class permisosAdministrador(BasePermission):
    """
    Permite acceso solo a usuarios con rol Administrador
    """
    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        if not user or not getattr(user, "is_authenticated", False):
            return False
        return user.rol == "Administrador"


class permisosUsuarios(BasePermission):
    """
    Permite acceso a cualquier usuario autenticado
    """
    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        return bool(user and getattr(user, "is_authenticated", False))
