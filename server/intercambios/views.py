from core.utils import get_error_response, get_success_response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import SolicitudRespuesta
from .serializers import (IntercambioSerializer, SolicitudRespuestaSerializer,
                          SolicitudSerializer)


class SolicitudAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = SolicitudSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return get_success_response("Solicitud created successfully.")
        else:
            return get_error_response("Solicitud creation failed.")


class SolicitudRespuestaAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Solo para usuarios autenticados

    def post(self, request, *args, **kwargs):
        serializer = SolicitudRespuestaSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return get_success_response("SolicitudRespuesta created successfully.")
        else:
            return get_error_response("SolicitudRespuesta creation failed.")

    def get(self, request, *args, **kwargs):
        solicitud_respuesta_id = kwargs.get("pk")
        solicitud_respuesta = get_object_or_404(
            SolicitudRespuesta, pk=solicitud_respuesta_id
        )

        # Verify that the user has permission to view this solicitud
        if solicitud_respuesta.administracion != request.user.administracion:
            return get_error_response(
                "You do not have permission to access this resource."
            )

        SolicitudRespuestaSerializer(solicitud_respuesta)
        return get_success_response("SolicitudRespuesta fetched successfully.")


class IntercambioAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = IntercambioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return get_success_response(
                "Intercambio created and completed successfully."
            )
        else:
            return get_error_response("Intercambio creation failed.")
