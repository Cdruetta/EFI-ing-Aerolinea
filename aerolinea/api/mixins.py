from rest_framework.permissions import IsAuthenticated, IsAdminUser


class AuthView:
    """
    Clase base para las vistas que requiere autenticación
    """
    permission_classes = [IsAuthenticated]


class AuthAdminView:
    """
    Clase base para las vistas que requiere autenticación de un usuario Admin
    """
    permission_classes = [IsAdminUser]