from rest_framework.permissions import BasePermission


class IsOwnerOrRelated(BasePermission):
    """
    Custom permission to allow users to edit only their ownSolicitud or Respuesta related to their Solicitud.
    """

    def has_object_permission(self, request, view, obj):
        # Case 1: If the object is a Request, the user must be the owner
        if hasattr(obj, "administracion") and obj.administracion == request.user.administracion:
            return True

        # Case 2: If the object is a Response, it must be related to a Request
        # of the user (even if they are not the owner of the Response).
        if hasattr(obj, "solicitud") and obj.solicitud.administracion == request.user.administracion:
            return True

        return False


class IsAdminOrOwnAdministracion(BasePermission):
    """
    Allows access only to superusers or users who belong to the same administration as the request.
    """
    def has_object_permission(self, request, view, obj):
        # Allow access to superusers
        if request.user.is_superuser:
            return True

        # Allow access if the administration of the request matches that of the user
        return obj.administracion == request.user.administracion


class IsAdminOrIsOwner(BasePermission):
    """
    Allows access if the user is an administrator or is the owner of the resource.
    """
    def has_object_permission(self, request, view, obj):
        # Allow access if the user is an administrator
        if request.user.is_staff or request.user.is_superuser:
            return True

        # Allow access if the user is the owner of the object (assuming the object has an 'owner' field)
        return obj.owner == request.user
