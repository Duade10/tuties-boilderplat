from rest_framework.permissions import BasePermission


class IsObjectUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        print(obj.user, request.user)
        return obj.user == request.user
