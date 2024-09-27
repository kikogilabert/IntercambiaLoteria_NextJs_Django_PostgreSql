from typing import Any, Dict, Optional

from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    AdministracionRegisterSerializer,
    UsuarioRegisterSerializer,
    UsuarioSerializer,
)


# User Registration View
class UsuarioRegisterView(APIView):
    def post(self, request):
        # Check if administracion data exist.
        administracion_data = request.data.get("administracion")
        if not administracion_data:
            return Response(
                {"error": "Datos de administracion son requeridos."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if usuarios data exist.
        usuario_data = request.data.get("usuario")
        if not administracion_data:
            return Response(
                {"error": "Datos de usuario son requeridos."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Begin the transaction to ensure atomicity
        with transaction.atomic():
            # Create and save the Administracion object first
            administracion_serializer = AdministracionRegisterSerializer(
                data=administracion_data
            )
            if administracion_serializer.is_valid():
                administracion = (
                    administracion_serializer.save()
                )  # Save the administracion

                # Now we have administracion.id, add it to usuario_data
                usuario_data["id_administracion"] = administracion.id
            else:
                return Response(
                    administracion_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            # Validate and create the Usuario object
            usuario_serializer = UsuarioRegisterSerializer(data=usuario_data)
            if usuario_serializer.is_valid():
                usuario_serializer.save()  # Save the usuario
                correct_data = {
                    "administracion": administracion_serializer.data,
                    "usuario": usuario_serializer.data,
                }
                return Response(
                    {"message": "User created successfully", "data": correct_data},
                    status=status.HTTP_201_CREATED,
                )
            else:
                # If usuario data is invalid, raise an error
                return Response(
                    usuario_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )


# User Login View (uses token-based authentication)
class UsuarioLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
        )


# User Profile Update View
class UsuarioUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    # PUT method to fully or partially update the user
    def put(self, request):
        serializer = UsuarioSerializer(
            request.user, data=request.data, partial=False
        )  # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User updated successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PATCH method for partial updates
    def patch(self, request):
        serializer = UsuarioSerializer(
            request.user, data=request.data, partial=True
        )  # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User updated successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # New function to deactivate the user
    def delete(self, request):
        user = request.user
        user.is_active = False  # Deactivate the user
        user.save()

        return Response(
            {"message": "User deactivated successfully"}, status=status.HTTP_200_OK
        )
