from rest_framework import permissions
from rest_framework.views import View, Request
from .models import Account


class IsCritic(permissions.BasePermission):
    def has_permission(self, request: Request, views: View) -> bool:

        if not request.user.id:
            return False

        return request.user.is_critic


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_superuser


class IsCriticOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:

        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user.id:
            return False

        return request.user.is_critic


class IsCriticOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, user:Account) -> bool:

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_critic:
            return True

        return request.user == user.user
