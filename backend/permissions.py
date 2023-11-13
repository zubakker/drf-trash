from drf_yasg import openapi

from rest_framework.permissions import (BasePermission, AllowAny, 
            IsAuthenticated, IsAdminUser)


authorization_header = openapi.Parameter('Authorization', openapi.IN_HEADER, 
                         description="Access token", 
                         type=openapi.TYPE_STRING)

class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return True

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        if not obj.user:
            return False
        if request.user.id == obj.user.id:
            return True
        return False

# class ReadOnly(BasePermission):

