from rest_framework.permissions import BasePermission


class IsOwnerOrRelated(BasePermission):
    """
    Permiso personalizado para permitir que los usuarios editen solo su propia
    Solicitud o una Respuesta relacionada con su Solicitud.
    """

    def has_object_permission(self, request, view, obj):
        # Caso 1: Si el objeto es una Solicitud, el usuario debe ser el propietario
        if hasattr(obj, "administracion") and obj.administracion == request.user.administracion:
            return True

        # Caso 2: Si el objeto es una Respuesta, debe estar relacionada con una Solicitud
        # del usuario (aunque no sea el propietario de la Respuesta).
        if hasattr(obj, "solicitud") and obj.solicitud.administracion == request.user.administracion:
            return True

        return False
