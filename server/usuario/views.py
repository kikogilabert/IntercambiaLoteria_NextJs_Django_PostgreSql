from django.db import transaction
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from usuario.models import Administracion
from usuario.serializers import (
    AdministracionRegisterSerializer,
    AdministracionSerializer,
    ChangePasswordSerializer,
    UsuarioLoginSerializer,
    UsuarioRegisterSerializer,
    UsuarioSerializer,
)

from core.utils import get_error_response, get_success_response


# User Registration View
class UsuarioRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Check if administracion data exist.
        administracion_data = request.data.get("administracion")
        if not administracion_data:
            return get_error_response("Datos de administracion son requeridos.")

        # Check if usuarios data exist.
        usuario_data = request.data.get("usuario")
        if not administracion_data:
            return get_error_response("Datos de usuario son requeridos.")

        # Begin the transaction to ensure atomicity
        with transaction.atomic():
            # Create and save the Administracion object first
            administracion_serializer = AdministracionRegisterSerializer(data=administracion_data)
            if administracion_serializer.is_valid():
                administracion = administracion_serializer.save()  # Save the administracion

                # Now we have administracion.id, add it to usuario_data
                usuario_data["administracion"] = administracion.id
            else:
                return get_error_response(
                    "Error en la validacion de los datos de administración.", data=administracion_serializer.errors
                )

            # Validate and create the Usuario object
            usuario_serializer = UsuarioRegisterSerializer(data=usuario_data)
            if usuario_serializer.is_valid():
                usuario_serializer.save()  # Save the usuario
                correct_data = {"administracion": administracion_serializer.data, "usuario": usuario_serializer.data}
                return get_success_response("User created successfully", data=correct_data)
            else:
                # If usuario data is invalid, raise an error
                return get_error_response(
                    "Error en la validacion de los datos de Usuario.", data=usuario_serializer.errors
                )


# User Login View using JWT
class UsuarioLoginView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to access this view

    def post(self, request):
        serializer = UsuarioLoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data
            tokens = serializer.get_tokens(user)

            return get_success_response(
                "Sesion correctamente iniciada con el usuario.",
                data={"access_token": tokens["access"], "refresh_token": tokens["refresh"]},
            )

        return get_error_response("Error en la validacion de email y/o contraseña.", data=serializer.errors)


# User Profile Update View
class UsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    # Get the user profile
    def get(self, request):
        user = request.user
        serializer = UsuarioSerializer(user)
        return get_success_response(message="Usuario retornado correctamente.", data=serializer.data)

    # PUT method to fully update the user
    def put(self, request):
        serializer = UsuarioSerializer(request.user, data=request.data, partial=False)  # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return get_success_response(message="Usuario actualizado correctamente.")
        return get_error_response(message="Error en la actualización del usuario.", data=serializer.errors)

    # PATCH method for partial updates on the user
    def patch(self, request):
        serializer = UsuarioSerializer(request.user, data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return get_success_response(message="Usuario actualizado correctamente.")
        return get_error_response(message="Error en la actualización del usuario.", data=serializer.errors)

    # New function to deactivate the user
    def delete(self, request):
        user = request.user
        user.is_active = False  # Deactivate the user
        user.save()

        return get_success_response(message="Usuario desactivado.")


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return get_success_response(message="Contraseña actualizada correctamente.")
        return get_error_response(message="Error en la actualización de la contraseña.", data=serializer.errors)


# Administracion Update View
class AdministracionView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, id_administracion):
        try:
            return Administracion.objects.get(id=id_administracion)
        except Administracion.DoesNotExist:
            return None

    # Get the user profile
    def get(self, request, id_administracion):
        print(id_administracion)
        administracion = self.get_object(id_administracion)
        if not administracion:
            return get_error_response(message="Administración no encontrada.", data=None)
        print(administracion)
        serializer = AdministracionSerializer(administracion)
        return get_success_response(message="Administracion retornada correctamente.", data=serializer.data)

    # PUT method to fully update the user
    def put(self, request, id_administracion):
        administracion = self.get_object(id_administracion)
        if not administracion:
            return get_error_response(message="Administración no encontrada.", data=None)
        serializer = AdministracionSerializer(administracion, data=request.data, partial=False)  # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return get_success_response(message="Administración actualizada correctamente.")
        return get_error_response(message="Error en la actualización de la administración.", data=serializer.errors)

    # PATCH method for partial updates on the user
    def patch(self, request, id_administracion):
        administracion = self.get_object(id_administracion)
        if not administracion:
            return get_error_response(message="Administración no encontrada.", data=None)
        serializer = AdministracionSerializer(administracion, data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return get_success_response(message="Administración actualizada correctamente.")
        return get_error_response(message="Error en la actualización de la administración.", data=serializer.errors)

    # New function to deactivate the user
    # def delete(self, request):
    #     user = request.user
    #     user.is_active = False  # Deactivate the user
    #     user.save()

    #     return Response(
    #         {"message": "User deactivated successfully"}, status=status.HTTP_200_OK
    #     )
