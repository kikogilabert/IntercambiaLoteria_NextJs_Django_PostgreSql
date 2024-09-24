from typing import Any, Dict, Optional

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
)
from rest_framework.request import Request
from rest_framework.response import Response
from django.db import transaction
from .models import Usuario
from .serializers import UsuarioSerializer, AdministracionSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    administracion_serializer_class = AdministracionSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        
        administracion_data = request.data.get('administracion')
        if not administracion_data:
            return Response({"error": "Datos de administracion son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

        usuario_data = request.data.get('usuario')
        if not administracion_data:
            return Response({"error": "Datos de usuario son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

        # Create Administracion
        administracion_serializer = self.administracion_serializer_class(data=administracion_data)
        administracion_serializer.is_valid(raise_exception=True)
        administracion = administracion_serializer.save()

        # Create Usuario
        usuario_data['id_administracion'] = administracion.id
        usuario_serializer = self.get_serializer(data=usuario_data)
        usuario_serializer.is_valid(raise_exception=True)
        self.perform_create(usuario_serializer)

        headers = self.get_success_headers(usuario_serializer.data)
        return Response(usuario_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# class UsuarioViewSet(viewsets.ModelViewSet):
#     """
#     A ViewSet for viewing, creating, updating, and deleting Usuario instances.

#     Provides endpoints to register new users, retrieve user details, update user
#     information, delete users, and perform custom actions like deactivating a user.
#     """

#     queryset = Usuario.objects.all()
#     serializer_class = UsuarioSerializer
#     administracion_serializer_class = AdministracionSerializer

#     def get_permissions(self) -> list:
#         """
#         Determine the permissions required for each action.

#         Returns:
#             list: A list of permission instances.
#         """
#         if self.action == 'create':
#             return [AllowAny()]
#         elif self.action in ['destroy', 'update', 'partial_update']:
#             return [IsAdminUser()]
#         else:
#             return [IsAuthenticated()]

#     def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
#         """
#         Handle user registration by creating a new Usuario instance.

#         Args:
#             request (Request): The HTTP request containing user data.
#             *args (Any): Variable length argument list.
#             **kwargs (Any): Arbitrary keyword arguments.

#         Returns:
#             Response: A DRF Response object with a success message and user data.
#         """
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         # Hash the password before saving
#         serializer.save()

#         headers = self.get_success_headers(serializer.data)
#         return Response(
#             {"message": "Usuario registrado exitosamente", "data": serializer.data},
#             status=status.HTTP_201_CREATED,
#             headers=headers
#         )

#     def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
#         """
#         Retrieve a specific Usuario instance.

#         Args:
#             request (Request): The HTTP request.
#             *args (Any): Variable length argument list.
#             **kwargs (Any): Arbitrary keyword arguments.

#         Returns:
#             Response: A DRF Response object with the serialized user data.
#         """
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)

#     def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
#         """
#         Update an existing Usuario instance.

#         Args:
#             request (Request): The HTTP request containing updated data.
#             *args (Any): Variable length argument list.
#             **kwargs (Any): Arbitrary keyword arguments.

#         Returns:
#             Response: A DRF Response object with a success message and updated user data.
#         """
#         partial: bool = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         return Response(
#             {"message": "Usuario actualizado exitosamente", "data": serializer.data}
#         )

#     def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
#         """
#         Delete a specific Usuario instance.

#         Args:
#             request (Request): The HTTP request.
#             *args (Any): Variable length argument list.
#             **kwargs (Any): Arbitrary keyword arguments.

#         Returns:
#             Response: A DRF Response object with a success message.
#         """
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response(
#             {"message": "Usuario eliminado exitosamente"},
#             status=status.HTTP_200_OK
#         )

#     @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
#     def deactivate(self, request: Request, pk: Optional[int] = None) -> Response:
#         """
#         Custom action to deactivate a Usuario instance.

#         Args:
#             request (Request): The HTTP request.
#             pk (Optional[int]): The primary key of the user to deactivate.

#         Returns:
#             Response: A DRF Response object with a success message.
#         """
#         user = self.get_object()
#         user.is_active = False
#         user.save()
#         return Response(
#             {"message": "Usuario desactivado"},
#             status=status.HTTP_200_OK
#         )
