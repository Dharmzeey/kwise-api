from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class IsUserVerified(BasePermission):
    message = "User email not verified."

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if not request.user.email_verified:
                raise PermissionDenied(detail=self.message)
            return True
        return False


