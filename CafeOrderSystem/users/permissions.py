from rest_framework import permissions
from .models import User


class isAccountOwnerPermission(permissions.BasePermission):
    pass


class isOrderOwnerPermission(permissions.BasePermission):
    pass

class isStaffPermission(permissions.BasePermission):
    pass

class isManagerPermission(permissions.BasePermission):
    pass