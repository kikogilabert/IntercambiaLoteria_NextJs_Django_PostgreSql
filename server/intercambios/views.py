from django.db import transaction
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from intercambios.constants import ESTADOS_RESPUESTA, ESTADOS_SOLICITUD
from intercambios.filters import SolicitudFilter  # Importa tu filtro
from intercambios.models import Intercambio, Respuesta, Solicitud
from intercambios.permissions import IsAdminOrOwnAdministracion, IsOwnerOrRelated
from intercambios.serializers import IntercambioSerializer, RespuestaSerializer, SolicitudSerializer

from core.utils import get_error_response, get_success_response
from core.views import ChangeStateAPIView


class SolicitudAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Instantiate and return the appropriate permission classes for each method (GET, PUT, PATCH).
        """
        if self.request.method in ["GET", "PUT", "PATCH"]:
            return [IsAuthenticated(), IsAdminOrOwnAdministracion()]
        return super().get_permissions()

    def post(self, request, *args, **kwargs):
        """
        Create a new request.
        """
        serializer = SolicitudSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return get_error_response("La creación de la solicitud falló.", data=serializer.errors)

        serializer.save()
        return get_success_response("Solicitud creada exitosamente.")

    def get(self, request, *args, **kwargs):
        """
        Get a request by its ID.
        """
        try:
            solicitud_id = kwargs.get("pk")
            solicitud = get_object_or_404(Solicitud, pk=solicitud_id)
            serializer = SolicitudSerializer(solicitud)
            return get_success_response(data=serializer.data)
        except Exception as e:
            return get_error_response(f"Ocurrió un error inesperado: {str(e)}", status_code=500)

    def put(self, request, *args, **kwargs):
        """
        Update an existing request.
        """
        try:
            solicitud_id = kwargs.get("pk")
            solicitud = get_object_or_404(Solicitud, pk=solicitud_id)
            serializer = SolicitudSerializer(solicitud, data=request.data, context={"request": request})
            if not serializer.is_valid():
                return get_error_response("La actualización de la solicitud falló.", data=serializer.errors)
            serializer.save()
            return get_success_response("Solicitud actualizada exitosamente.", data=serializer.data)
        except Exception as e:
            return get_error_response(f"Ocurrió un error inesperado: {str(e)}", status_code=500)

    def patch(self, request, *args, **kwargs):
        """
        Partially update an existing request.
        """
        try:
            solicitud_id = kwargs.get("pk")
            solicitud = get_object_or_404(Solicitud, pk=solicitud_id)
            serializer = SolicitudSerializer(solicitud, data=request.data, partial=True, context={"request": request})
            if not serializer.is_valid():
                return get_error_response("La actualización parcial de la solicitud falló.", data=serializer.errors)
            serializer.save()
            return get_success_response("Solicitud actualizada parcialmente con éxito.", data=serializer.data)
        except Exception as e:
            return get_error_response(f"Ocurrió un error inesperado: {str(e)}", status_code=500)


class SolicitudFilterView(ListAPIView):
    """
    Get all requests or filter by parameters.
    """

    queryset = Solicitud.objects.all()  # Get all requests by default
    serializer_class = SolicitudSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = SolicitudFilter  # Use the filter defined in filters.py


class RespuestaAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Instantiate and return the appropriate permission classes for each method (GET, PUT, PATCH).
        """
        if self.request.method in ["GET", "PUT", "PATCH"]:
            return [IsAuthenticated(), IsAdminOrOwnAdministracion()]
        return super().get_permissions()

    def post(self, request, *args, **kwargs):
        """
        Create a new response.
        """
        serializer = RespuestaSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return get_error_response("La creación de la respuesta falló.", data=serializer.errors)

        serializer.save()
        return get_success_response("Respuesta creada exitosamente.")

    def get(self, request, *args, **kwargs):
        """
        Get a response by its ID.
        """
        try:
            respuesta_id = kwargs.get("pk")
            respuesta = get_object_or_404(Respuesta, pk=respuesta_id)
            serializer = RespuestaSerializer(respuesta)
            return get_success_response(data=serializer.data)
        except Exception as e:
            return get_error_response(f"Ocurrió un error inesperado: {str(e)}", status_code=500)

    def put(self, request, *args, **kwargs):
        """
        Update an existing response.
        """
        try:
            respuesta_id = kwargs.get("pk")
            respuesta = get_object_or_404(Respuesta, pk=respuesta_id)
            serializer = RespuestaSerializer(respuesta, data=request.data, context={"request": request})
            if not serializer.is_valid():
                return get_error_response("La actualización de la respuesta falló.", data=serializer.errors)
            serializer.save()
            return get_success_response("Respuesta actualizada exitosamente.", data=serializer.data)
        except Exception as e:
            return get_error_response(f"Ocurrió un error inesperado: {str(e)}", status_code=500)

    def patch(self, request, *args, **kwargs):
        """
        Partially update an existing response.
        """
        try:
            respuesta_id = kwargs.get("pk")
            respuesta = get_object_or_404(Respuesta, pk=respuesta_id)
            serializer = RespuestaSerializer(respuesta, data=request.data, partial=True, context={"request": request})
            if not serializer.is_valid():
                return get_error_response("La actualización parcial de la respuesta falló.", data=serializer.errors)
            serializer.save()
            return get_success_response("Respuesta actualizada parcialmente con éxito.", data=serializer.data)
        except Exception as e:
            return get_error_response(f"Ocurrió un error inesperado: {str(e)}", status_code=500)


class IntercambioAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """
        Create a new exchange when a request and its response are accepted.
        """
        serializer = IntercambioSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return get_error_response("La creación del intercambio falló.", data=serializer.errors)

        try:
            serializer.save()
            return get_success_response("Intercambio creado exitosamente.", data=serializer.data)
        except serializers.ValidationError as e:
            return get_error_response(str(e))
        except Exception as e:
            return get_error_response(
                f"Ocurrió un error inesperado: {str(e)}", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get(self, request, *args, **kwargs):
        """
        Get an exchange by its ID or list all exchanges.
        """
        intercambio_id = kwargs.get("pk")

        try:
            if intercambio_id:
                intercambio = get_object_or_404(Intercambio, pk=intercambio_id)
                serializer = IntercambioSerializer(intercambio)
                return get_success_response(data=serializer.data)

            # If no pk is provided, get all instances
            intercambios = Intercambio.objects.all()
            serializer = IntercambioSerializer(intercambios, many=True)
            return get_success_response(data=serializer.data)
        except Exception as e:
            return get_error_response(
                f"Ocurrió un error al obtener el intercambio: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ChangeSolicitudStateAPIView(ChangeStateAPIView):
    """View to change the state of a Solicitud."""

    permission_classes = [IsAuthenticated, IsOwnerOrRelated]

    def get_model_class(self):
        return Solicitud

    def get_valid_transitions(self):
        # Define valid states for state transition in Solicitud
        return [estado[0] for estado in ESTADOS_SOLICITUD]


class ChangeRespuestaStateAPIView(ChangeStateAPIView):
    """
    View to change the state of a Respuesta.
    """

    permission_classes = [IsAuthenticated, IsOwnerOrRelated]

    def get_model_class(self):
        return Respuesta

    def get_valid_transitions(self):
        # Define valid states for state transition in Respuesta
        return [estado[0] for estado in ESTADOS_RESPUESTA]
