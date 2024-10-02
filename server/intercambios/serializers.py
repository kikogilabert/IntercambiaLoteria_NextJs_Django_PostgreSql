from rest_framework import serializers
from .models import Sorteo, Solicitud, SolicitudRespuesta, Intercambio, LoteriaIntercambio


class SorteoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sorteo
        fields = ['id', 'codigo', 'fecha', 'precio']


class SolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = ['id', 'tipo', 'administracion', 'numero', 'num_series', 'sorteo', 'condicion', 'num_cond', 'num_series_cond', 'sorteo_cond', 'estado', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class SolicitudRespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitudRespuesta
        fields = ['id', 'solicitud', 'administracion', 'numero', 'num_series', 'sorteo', 'estado', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class IntercambioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intercambio
        fields = ['id', 'solicitud', 'solicitud_respuesta', 'origen', 'destino', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class LoteriaIntercambioSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoteriaIntercambio
        fields = ['id', 'administracion', 'numero', 'num_series', 'sorteo']
