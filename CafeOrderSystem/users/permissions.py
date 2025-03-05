from rest_framework.permissions import BasePermission
from .models import User


class isAccountOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        
        return request.user == obj.user