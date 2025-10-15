from rest_framework.permissions import BasePermission

class HasAPIKeyOrIsAuthenticated(BasePermission):
    """
    Разрешение: либо по API-ключу, либо по JWT-токену.
    """
    def has_permission(self, request, view):
        # Проверка токена (JWT)
        if request.user and request.user.is_authenticated:
            return True

        # Проверка API-ключа в заголовке
        api_key = request.headers.get("X-API-Key")
        return api_key == "SUPER_SECRET_KEY"  # можно вынести в settings
