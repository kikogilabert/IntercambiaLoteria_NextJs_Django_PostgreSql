# core/serializers.py

from rest_framework import serializers

from core.models import ComunidadAutonoma, Pais, Provincia


class ProvinciaSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provincia
        fields = ["id", "nombre", "codigo"]


class ProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provincia
        fields = ["id", "nombre", "codigo", "comunidad_autonoma", "pais"]


class ComunidadAutonomaSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComunidadAutonoma
        fields = ["id", "nombre", "codigo"]


class ComunidadAutonomaSerializer(serializers.ModelSerializer):
    provincias = ProvinciaSerializer(many=True, read_only=True)

    class Meta:
        model = ComunidadAutonoma
        fields = ["id", "nombre", "codigo", "pais", "provincias"]


class PaisSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pais
        fields = ["id", "nombre", "codigo"]


class PaisSerializer(serializers.ModelSerializer):
    comunidades_autonomas = ComunidadAutonomaSerializer(many=True, read_only=True)
    provincias = serializers.SerializerMethodField()

    class Meta:
        model = Pais
        fields = ["id", "nombre", "codigo", "comunidades_autonomas", "provincias"]

    # Método para obtener las provincias si no hay comunidades autónomas
    def get_provincias(self, obj):
        # Solo incluir provincias directamente bajo el país si no tiene comunidades autónomas
        if not obj.comunidades_autonomas.exists():
            provincias = Provincia.objects.filter(pais=obj)
            return ProvinciaSerializer(provincias, many=True).data
        return []
