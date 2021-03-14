from rest_framework import permissions


class IsAuthenticatedExceptForGET(permissions.BasePermission):
    """
        Custom permission class by installing it, authentication will not be required for 'GET' request
        rest for all request authentication will be required.
    """
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user and request.user.is_authenticated
