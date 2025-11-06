from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """Permite acceso solo a administradores."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'rol', '') == 'admin'


class IsCliente(permissions.BasePermission):
    """Permite acceso solo a clientes."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'rol', '') == 'cliente'

