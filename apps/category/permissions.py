from rest_framework.permissions import BasePermission


class CategoryPermissions(BasePermission):
    protected_methods = ("POST", "GET", "PATCH", "PUT", "DELETE")

    def has_permission(self, request, _):
        user = request.user
        method = request.method

        if not user.is_authenticated and method in self.protected_methods:
            return False

        return True
