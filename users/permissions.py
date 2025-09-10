from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSeller(BasePermission):
    """
    Custom permission to only allow sellers to edit their own products.
    """

    def has_permission(self, request, view): # type: ignore
        return bool(request.user and request.user.is_authenticated and request.user.role == 'seller')

