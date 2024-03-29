from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated


class IsAdministrator(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
            return request.user.id_role.id == 1 or request.user.id_role.id == 2 or request.user.id_role.id == 3  
        return request.user.role.id == 2

    
class IsEmployee(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.role.id == 3
        return request.user.role.id == 3
        
          
class IsPattient(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role.id == 1