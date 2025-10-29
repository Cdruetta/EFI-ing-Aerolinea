from django.conf import settings
from rest_framework.permissions import BasePermission
import logging

logger = logging.getLogger(__name__)

LOCAL_VALID_TOKENS = [
    "token-valido-1234",
    "777777",
]

class TokenPermission(BasePermission):
    message = "Token no válido"

    def _get_valid_tokens(self):
        return getattr(settings, "VALID_TOKENS", LOCAL_VALID_TOKENS)

    def has_permission(self, request, view):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            logger.debug("TokenPermission: no Authorization header")
            return False

        parts = auth_header.split()
        if len(parts) != 2:
            logger.debug("TokenPermission: Authorization header con formato inválido: %r", auth_header)
            return False

        scheme, token = parts[0].lower(), parts[1].strip()
        if scheme != "bearer":
            logger.debug("TokenPermission: esquema no soportado: %s", scheme)
            return False

        valid_tokens = self._get_valid_tokens()
        allowed = token in valid_tokens
        if not allowed:
            logger.debug("TokenPermission: token no válido: %s", token)
        return allowed

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
