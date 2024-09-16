from rest_framework import serializers
from .models import Administracion, Propietario
from django.core.validators import EmailValidator

class PropietarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Propietario
        fields = ['dni', 'nombre', 'telefono', 'direccion', 'tipo_propietario' ]

    # def validate_dni(self, value):
    #     if len(value) != 9 or not value[-1].isalpha():
    #         raise serializers.ValidationError("DNI debe tener 9 caracteres y el último debe ser una letra")
    #     return value
        

class AdministracionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Administracion
        fields = ['id_administracion', 'num_receptor', 'password', 'nombre_comercial', 
                    'direccion', 'localidad', 'provincia', 'numero_admon', 
                    'codigo_postal', 'propietario', 'email', 'telefono', 'created_at', 
                    'is_active']
    def validate_email(self, value):
        validator = EmailValidator()
        validator(value)
        if Administracion.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo electrónico ya está en uso")
        return value

    # def validate_telefono(self, value):
        # if len(value) != 9:
        #     raise serializers.ValidationError("El número de teléfono debe tener 9 dígitos")
        # return value

    # def validate_codigo_postal(self, value):
    #     if len(value) != 5:
    #         raise serializers.ValidationError("El código postal debe tener 5 dígitos")
    #     return value