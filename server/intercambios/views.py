from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as st
from django.shortcuts import get_object_or_404
from .models import Sorteo, Solicitud, SolicitudRespuesta, Intercambio, LoteriaIntercambio
from .serializers import SorteoSerializer, SolicitudSerializer, SolicitudRespuestaSerializer, IntercambioSerializer, LoteriaIntercambioSerializer
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from core.utils import ResponseStruct

# Helper function to update status of Solicitud and SolicitudRespuesta
def update_solicitud_respuesta_status(solicitud, solicitud_respuesta, intercambios_restantes):
    # Si es el último intercambio
    if intercambios_restantes == 1:
        solicitud.estado = 'completada'
        solicitud_respuesta.estado = 'completada'
    else:
        solicitud.estado = 'completada'
        solicitud_respuesta.estado = 'cancelada'
    solicitud.save()
    solicitud_respuesta.save()

class SolicitudAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        tipo_solicitud = data.get('tipo')
        condicion = data.get('condicion')
        
        if 'sorteo' not in data and condicion != "cesion":
            return ResponseStruct(
                        status="error",
                        message="Sorteo is required for this condition.",
                        error_code=st.HTTP_400_BAD_REQUEST
                    ).to_response()
        sorteo = data.get('sorteo')
        
        # Validar solicitud tipo 'enviar'
        if tipo_solicitud == "enviar":

            if condicion == "cesion":
                data['num_cond'] = None
                data['num_series_cond'] = None
                data['sorteo_cond'] = None
            elif condicion == "indiferente":
                data['num_cond'] = "XXXXX"
                data['num_series_cond'] = None
                data['sorteo_cond'] = sorteo
            elif condicion == "explicita":
                data['num_series_cond'] = None
                data['sorteo_cond'] = sorteo
        
        # Validar solicitud tipo 'recibir'
        elif tipo_solicitud == "recibir":
            if condicion == "cesion":
                data['num_cond'] = None
                data['num_series_cond'] = None
                data['sorteo_cond'] = None
            elif condicion == "explicita":
                data['num_series_cond'] = None
                data['sorteo_cond'] = sorteo

        # Serializar y guardar los datos
        serializer = SolicitudSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return ResponseStruct(
                status="success",
                message="Solicitud created successfully.",
                data=serializer.data,
                error_code=st.HTTP_201_CREATED
            ).to_response()

        return ResponseStruct(
            status="error",
            message="Solicitud creation failed.",
            data=serializer.errors,
            error_code=st.HTTP_400_BAD_REQUEST
        ).to_response()


class SolicitudRespuestaAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Solo para usuarios autenticados

    def post(self, request, *args, **kwargs):
        data = request.data
        
        # Obtener la solicitud asociada
        #solicitud_id = data.get('solicitud')
        #solicitud = get_object_or_404(Solicitud, pk=solicitud_id)

        # Serializar y guardar los datos de SolicitudRespuesta
        serializer = SolicitudRespuestaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return ResponseStruct(
                status="success",
                message="SolicitudRespuesta created successfully.",
                data=serializer.data,
                error_code=st.HTTP_201_CREATED
            ).to_response()

        return ResponseStruct(
            status="error",
            message="SolicitudRespuesta creation failed.",
            data=serializer.errors,
            error_code=st.HTTP_400_BAD_REQUEST
        ).to_response()

    def get(self, request, *args, **kwargs):
        solicitud_respuesta_id = kwargs.get('pk')
        solicitud_respuesta = get_object_or_404(SolicitudRespuesta, pk=solicitud_respuesta_id)
        serializer = SolicitudRespuestaSerializer(solicitud_respuesta)
        return ResponseStruct(
            status="success",
            message="SolicitudRespuesta fetched successfully.",
            data=serializer.data,
            error_code=st.HTTP_200_OK
        ).to_response()


class IntercambioAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data

        if 'solicitud' not in data or 'solicitud_respuesta' not in data:
            return ResponseStruct(
                            status="error",
                            message="Solicitud y SolicitudRespuesta is required for this condition.",
                            error_code=st.HTTP_400_BAD_REQUEST
                        ).to_response()
        

        solicitud_id = data.get('solicitud')
        solicitud_respuesta_id = data.get('solicitud_respuesta')

        # Obtener solicitud y solicitud_respuesta
        solicitud = get_object_or_404(Solicitud, pk=solicitud_id)
        solicitud_respuesta = get_object_or_404(SolicitudRespuesta, pk=solicitud_respuesta_id)

        # Verificar si ambas partes han aceptado
        if solicitud.estado != 1 or solicitud_respuesta.estado != 1:
            return ResponseStruct(
                status="error",
                message="Both Solicitud and SolicitudRespuesta must be accepted before creating an intercambio.",
                error_code=st.HTTP_400_BAD_REQUEST
            ).to_response()

        # Validar tipo de solicitud
        tipo_solicitud = solicitud.tipo
        if tipo_solicitud == "enviar":
            data['origen'] = {
                'numero': solicitud.numero,
                'num_series': solicitud.num_series,
                'sorteo': solicitud.sorteo.codigo
            }
            data['destino'] = {
                'numero': solicitud_respuesta.numero,
                'num_series': solicitud_respuesta.num_series,
                'sorteo': solicitud_respuesta.sorteo.codigo
            }
        elif tipo_solicitud == "recibir":
            data['origen'] = {
                'numero': solicitud.num_cond,
                'num_series': solicitud.num_series_cond,
                'sorteo': solicitud.sorteo_cond.codigo
            }
            data['destino'] = {
                'numero': solicitud_respuesta.numero,
                'num_series': solicitud_respuesta.num_series,
                'sorteo': solicitud_respuesta.sorteo.codigo
            }

        # Serializar y guardar el intercambio
        serializer = IntercambioSerializer(data=data)
        if serializer.is_valid():
            intercambio = serializer.save()

            # Intentar realizar el intercambio
            if intercambio.realizar_intercambio():
                return ResponseStruct(
                    status="success",
                    message="Intercambio created and completed successfully.",
                    data=serializer.data,
                    error_code=st.HTTP_201_CREATED
                ).to_response()

            return ResponseStruct(
                status="error",
                message="Intercambio could not be completed.",
                error_code=st.HTTP_400_BAD_REQUEST
            ).to_response()

        return ResponseStruct(
            status="error",
            message="Intercambio creation failed.",
            data=serializer.errors,
            error_code=st.HTTP_400_BAD_REQUEST
        ).to_response()

