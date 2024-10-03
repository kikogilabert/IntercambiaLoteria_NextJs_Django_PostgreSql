from django.db import transaction
from rest_framework import serializers
from usuario.models import Administracion

from .constants import ESTADO_ABIERTA, ESTADO_ACEPTADA
from .models import (Intercambio, LoteriaIntercambio, Solicitud,
                     SolicitudRespuesta, Sorteo)


class SorteoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sorteo
        fields = ["id", "codigo", "fecha", "precio"]


class SolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = [
            "id",
            "tipo",
            "administracion",
            "numero",
            "num_series",
            "sorteo",
            "condicion",
            "num_cond",
            "num_series_cond",
            "sorteo_cond",
            "estado",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "administracion",
            "estado",
            "created_at",
            "updated_at",
        ]

    def validate_numero(self, value):
        if len(value) != 5:
            raise serializers.ValidationError("Numero must be a 5-digit number.")
        return value

    def validate(self, data):
        tipo_solicitud = data.get("tipo")
        condicion = data.get("condicion")
        sorteo = data.get("sorteo")

        # 'sorteo' is required if 'condicion' != 0
        if condicion != 0 and not sorteo:
            raise serializers.ValidationError(
                {"sorteo": "Sorteo is required for this condition."}
            )

        # Validar solicitud tipo 'enviar'
        if tipo_solicitud == 0:
            if condicion == 0:  # Cesion
                data["num_cond"] = None
                data["num_series_cond"] = None
                data["sorteo_cond"] = None
            elif condicion == 1:  # Indiferente
                data["num_cond"] = "XXXXX"
                data["num_series_cond"] = None
                data["sorteo_cond"] = sorteo
            elif condicion == 2:  # Explícita
                data["num_series_cond"] = None
                data["sorteo_cond"] = sorteo

        # Validar solicitud tipo 'recibir'
        elif tipo_solicitud == 1:
            if condicion == 0:  # Cesion
                data["num_cond"] = None
                data["num_series_cond"] = None
                data["sorteo_cond"] = None
            elif condicion == 2:  # Explícita
                data["num_series_cond"] = None
                data["sorteo_cond"] = sorteo

        return data

    def create(self, validated_data):
        # Set 'administracion' from the authenticated user
        user = self.context["request"].user
        if hasattr(user, "administracion"):
            validated_data["administracion"] = user.administracion
        else:
            raise serializers.ValidationError(
                {"administracion": "User does not have an associated 'Administracion'."}
            )
        return super().create(validated_data)


class SolicitudRespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitudRespuesta
        fields = [
            "id",
            "solicitud",
            "administracion",
            "numero",
            "num_series",
            "sorteo",
            "estado",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "administracion",
            "estado",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        # Set 'administracion' from the authenticated user
        user = self.context["request"].user
        if hasattr(user, "administracion"):
            validated_data["administracion"] = user.administracion
        else:
            raise serializers.ValidationError(
                {"administracion": "User does not have an associated 'Administracion'."}
            )
        return super().create(validated_data)


class IntercambioSerializer(serializers.ModelSerializer):
    origen = serializers.PrimaryKeyRelatedField(
        queryset=LoteriaIntercambio.objects.all()
    )
    destino = serializers.PrimaryKeyRelatedField(
        queryset=LoteriaIntercambio.objects.all()
    )

    class Meta:
        model = Intercambio
        fields = [
            "id",
            "solicitud",
            "solicitud_respuesta",
            "origen",
            "destino",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "origen",
            "destino",
            "created_at",
            "updated_at",
        ]

    def validate(self, data):
        solicitud = data.get("solicitud")
        solicitud_respuesta = data.get("solicitud_respuesta")

        # Ensure both 'solicitud' and 'solicitud_respuesta' are provided
        if not solicitud or not solicitud_respuesta:
            raise serializers.ValidationError(
                "Both 'solicitud' and 'solicitud_respuesta' are required."
            )

        # Verify that both parties have accepted
        if solicitud.estado != ESTADO_ABIERTA or solicitud_respuesta.estado != ESTADO_ACEPTADA:
            raise serializers.ValidationError(
                "Both Solicitud and SolicitudRespuesta must be 'aceptada' before creating an intercambio."
            )

        # Check for existing Intercambio between the same Solicitud and SolicitudRespuesta
        if Intercambio.objects.filter(
            solicitud=solicitud, solicitud_respuesta=solicitud_respuesta
        ).exists():
            raise serializers.ValidationError(
                "An intercambio between this Solicitud and SolicitudRespuesta already exists."
            )

        return data

    def create(self, validated_data):
        solicitud = validated_data.get("solicitud")
        solicitud_respuesta = validated_data.get("solicitud_respuesta")

        # Determine the tipo_solicitud and prepare data for origen and destino
        tipo_solicitud = solicitud.tipo
        if tipo_solicitud == 0:  # Enviar
            origen_data = {
                "administracion": solicitud.administracion,
                "numero": solicitud.numero,
                "num_series": solicitud.num_series,
                "sorteo": solicitud.sorteo,
            }
            destino_data = {
                "administracion": solicitud_respuesta.administracion,
                "numero": solicitud_respuesta.numero,
                "num_series": solicitud_respuesta.num_series,
                "sorteo": solicitud_respuesta.sorteo,
            }
        elif tipo_solicitud == 1:  # Recibir
            origen_data = {
                "administracion": solicitud.administracion,
                "numero": solicitud.num_cond,
                "num_series": solicitud.num_series_cond,
                "sorteo": solicitud.sorteo_cond,
            }
            destino_data = {
                "administracion": solicitud_respuesta.administracion,
                "numero": solicitud_respuesta.numero,
                "num_series": solicitud_respuesta.num_series,
                "sorteo": solicitud_respuesta.sorteo,
            }
        else:
            raise serializers.ValidationError({"tipo": "Invalid 'tipo' in solicitud."})

        with transaction.atomic():
            # Create LoteriaIntercambio instances
            origen = LoteriaIntercambio.objects.create(**origen_data)
            destino = LoteriaIntercambio.objects.create(**destino_data)

            # Set 'origen' and 'destino' in validated_data
            validated_data["origen"] = origen
            validated_data["destino"] = destino

            # Create the Intercambio instance
            intercambio = super().create(validated_data)

            # Attempt to perform the intercambio
            if not intercambio.realizar_intercambio():
                raise serializers.ValidationError("Intercambio could not be completed due to invalid states.")

            return intercambio



class LoteriaIntercambioSerializer(serializers.ModelSerializer):
    administracion = serializers.PrimaryKeyRelatedField(
        queryset=Administracion.objects.all()
    )

    class Meta:
        model = LoteriaIntercambio
        fields = ["id", "administracion", "numero", "num_series", "sorteo"]
