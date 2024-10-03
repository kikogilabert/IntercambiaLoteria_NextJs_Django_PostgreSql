from core.utils import get_error_response, get_success_response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Respuesta
from .serializers import (IntercambioSerializer, RespuestaSerializer,
                          SolicitudSerializer)


class SolicitudAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = SolicitudSerializer(
            data=request.data, context={"request": request}
        )
        if not serializer.is_valid():
            return get_error_response("Solicitud creation failed.")
        
        serializer.save()
        return get_success_response("Solicitud created successfully.")


class RespuestaAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Solo para usuarios autenticados

    def post(self, request, *args, **kwargs):
        serializer = RespuestaSerializer(
            data=request.data, context={"request": request}
        )
        if not serializer.is_valid():
            return get_error_response("Respuesta creation failed.")
        
        serializer.save()
        return get_success_response("Respuesta created successfully.")

    def get(self, request, *args, **kwargs):
        solicitud_respuesta_id = kwargs.get("pk")
        solicitud_respuesta = get_object_or_404(
            Respuesta, pk=solicitud_respuesta_id
        )

        # Verify that the user has permission to view this solicitud
        if solicitud_respuesta.administracion != request.user.administracion:
            return get_error_response(
                "You do not have permission to access this resource."
            )

        RespuestaSerializer(solicitud_respuesta)
        return get_success_response("Respuesta fetched successfully.")


class IntercambioAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = IntercambioSerializer(data=request.data)
        if not serializer.is_valid():
            return get_error_response("Intercambio creation failed.")

        serializer.save()
        return get_success_response(
            "Intercambio created and completed successfully."
        )