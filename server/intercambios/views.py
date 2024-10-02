from core.utils import ResponseStruct
from django.shortcuts import get_object_or_404
from rest_framework import status as st
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import LoteriaIntercambio, Solicitud, SolicitudRespuesta
from .serializers import (IntercambioSerializer, SolicitudRespuestaSerializer,
                          SolicitudSerializer)


class SolicitudAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()

        try:
            tipo_solicitud = int(data.get("tipo"))
            condicion = int(data.get("condicion"))
        except (TypeError, ValueError):
            return ResponseStruct(
                status="error",
                message="Invalid 'tipo' or 'condicion' value.",
                error_code=st.HTTP_400_BAD_REQUEST,
            ).to_response()

        # Obtener la administracion del usuario autenticado
        if hasattr(request.user, "administracion"):
            data["administracion"] = request.user.administracion.id
        else:
            return ResponseStruct(
                status="error",
                message="User does not have an associated 'Administracion'.",
                error_code=st.HTTP_400_BAD_REQUEST,
            ).to_response()

        if "sorteo" not in data and condicion != 0:  # Cesion
            return ResponseStruct(
                status="error",
                message="Sorteo is required for this condition.",
                error_code=st.HTTP_400_BAD_REQUEST,
            ).to_response()
        sorteo = data.get("sorteo")

        # Validar solicitud tipo 'enviar'
        if tipo_solicitud == 0:
            if condicion == 0:  # Cesion
                data["num_cond"] = None
                data["num_series_cond"] = None
                data["sorteo_cond"] = None
            elif condicion == 1:  # indiferente
                data["num_cond"] = "XXXXX"
                data["num_series_cond"] = None
                data["sorteo_cond"] = sorteo
            elif condicion == 2:  # explicita
                data["num_series_cond"] = None
                data["sorteo_cond"] = sorteo

        # Validar solicitud tipo 'recibir'
        elif tipo_solicitud == 1:
            if condicion == 0:  # Cesion
                data["num_cond"] = None
                data["num_series_cond"] = None
                data["sorteo_cond"] = None
            elif condicion == 2:  # explicita
                data["num_series_cond"] = None
                data["sorteo_cond"] = sorteo

        # Serializar y guardar los datos
        serializer = SolicitudSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return ResponseStruct(
                message="Solicitud created successfully.",
                data=serializer.data,
            ).to_response()

        return ResponseStruct(
            status="error",
            message="Solicitud creation failed.",
            data=serializer.errors,
            error_code=st.HTTP_400_BAD_REQUEST,
        ).to_response()


class SolicitudRespuestaAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Solo para usuarios autenticados

    def post(self, request, *args, **kwargs):
        data = request.data.copy()

        # Obtener la solicitud asociada
        # solicitud_id = data.get('solicitud')
        # solicitud = get_object_or_404(Solicitud, pk=solicitud_id)

        # Asignar 'administracion' del usuario autenticado
        if hasattr(request.user, "administracion"):
            data["administracion"] = request.user.administracion.id
        else:
            return ResponseStruct(
                status="error",
                message="User does not have an associated 'Administracion'.",
                error_code=st.HTTP_400_BAD_REQUEST,
            ).to_response()

        # Serializar y guardar los datos de SolicitudRespuesta
        serializer = SolicitudRespuestaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return ResponseStruct(
                message="SolicitudRespuesta created successfully.",
                data=serializer.data,
            ).to_response()

        return ResponseStruct(
            status="error",
            message="SolicitudRespuesta creation failed.",
            data=serializer.errors,
            error_code=st.HTTP_400_BAD_REQUEST,
        ).to_response()

    def get(self, request, *args, **kwargs):
        solicitud_respuesta_id = kwargs.get("pk")
        solicitud_respuesta = get_object_or_404(
            SolicitudRespuesta, pk=solicitud_respuesta_id
        )

        # Verificar que el usuario tiene permiso para ver esta solicitud
        if solicitud_respuesta.administracion != request.user.administracion:
            return ResponseStruct(
                status="error",
                message="You do not have permission to access this resource.",
                error_code=st.HTTP_403_FORBIDDEN,
            ).to_response()

        serializer = SolicitudRespuestaSerializer(solicitud_respuesta)
        return ResponseStruct(
            message="SolicitudRespuesta fetched successfully.",
            data=serializer.data,
        ).to_response()


class IntercambioAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()

        if "solicitud" not in data or "solicitud_respuesta" not in data:
            return ResponseStruct(
                status="error",
                message="Solicitud y SolicitudRespuesta is required for this condition.",
                error_code=st.HTTP_400_BAD_REQUEST,
            ).to_response()

        solicitud_id = data.get("solicitud")
        solicitud_respuesta_id = data.get("solicitud_respuesta")

        # Obtener solicitud y solicitud_respuesta
        solicitud = get_object_or_404(Solicitud, pk=solicitud_id)
        solicitud_respuesta = get_object_or_404(
            SolicitudRespuesta, pk=solicitud_respuesta_id
        )

        # Verificar si ambas partes han aceptado
        if solicitud.estado != "aceptada" or solicitud_respuesta.estado != "aceptada":
            return ResponseStruct(
                status="error",
                message="Both Solicitud and SolicitudRespuesta must be 'aceptada' before creating an intercambio.",
                error_code=st.HTTP_400_BAD_REQUEST,
            ).to_response()

        # Validar tipo de solicitud
        tipo_solicitud = solicitud.tipo
        if tipo_solicitud == 0:  # Enviar
            origen_data = {
                "administracion": solicitud.administracion.id,
                "numero": solicitud.numero,
                "num_series": solicitud.num_series,
                "sorteo": solicitud.sorteo.id,
            }
            destino_data = {
                "administracion": solicitud_respuesta.administracion.id,
                "numero": solicitud_respuesta.numero,
                "num_series": solicitud_respuesta.num_series,
                "sorteo": solicitud_respuesta.sorteo.id,
            }
        elif tipo_solicitud == 1:  # Recibir
            origen_data = {
                "administracion": solicitud.administracion.id,
                "numero": solicitud.num_cond,
                "num_series": solicitud.num_series_cond,
                "sorteo": solicitud.sorteo_cond.id,
            }
            destino_data = {
                "administracion": solicitud_respuesta.administracion.id,
                "numero": solicitud_respuesta.numero,
                "num_series": solicitud_respuesta.num_series,
                "sorteo": solicitud_respuesta.sorteo.id,
            }

        origen = LoteriaIntercambio.objects.create(**origen_data)
        destino = LoteriaIntercambio.objects.create(**destino_data)
        data["origen"] = origen.id
        data["destino"] = destino.id

        # Serializar y guardar el intercambio
        serializer = IntercambioSerializer(data=data)
        if serializer.is_valid():
            intercambio = serializer.save()

            # Intentar realizar el intercambio
            if intercambio.realizar_intercambio():
                return ResponseStruct(
                    message="Intercambio created and completed successfully.",
                    data=serializer.data,
                ).to_response()

            return ResponseStruct(
                status="error",
                message="Intercambio could not be completed.",
                error_code=st.HTTP_400_BAD_REQUEST,
            ).to_response()

        return ResponseStruct(
            status="error",
            message="Intercambio creation failed.",
            data=serializer.errors,
            error_code=st.HTTP_400_BAD_REQUEST,
        ).to_response()
