from rest_framework import serializers
from boleto.models import Boleto

class BoletoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boleto
        fields = ['id', 'numero_boleto', 'series_boleto', 'num_series_disponibles', 'administracion']
        read_only_fields = ['id']

        