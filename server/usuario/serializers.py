import re
from typing import Any, Dict

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from usuario.models import (
    Administracion,  # Assuming your models are in models.py
    Usuario,
)

from core.constants import PROVINCIAS_CHOICES

########################################
############### PROFILE  ###############
########################################


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ["tipo", "dni", "nombre", "apellidos", "telefono", "email", "administracion"]


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, required=True)
    new_password1 = serializers.CharField(write_only=True, required=True)
    new_password2 = serializers.CharField(write_only=True, required=True)

    def validate_current_password(self, value):
        user = self.context["request"].user
        if not check_password(value, user.password):
            raise serializers.ValidationError("Current password is incorrect.")
        return value

    def validate(self, data):
        # Validate new passwords match
        new_password1 = data.get("new_password1")
        new_password2 = data.get("new_password2")
        if new_password1 != new_password2:
            raise serializers.ValidationError({"new_password": "New passwords do not match."})

        # Validate new password length
        if len(new_password1) < 8:
            raise serializers.ValidationError({"new_password": "New password must be at least 8 characters long."})

        return data

    def save(self, **kwargs):
        user = self.context["request"].user
        new_password = self.validated_data["new_password1"]
        user.set_password(new_password)
        user.save()
        return user


class AdministracionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administracion
        fields = [
            "nombre_comercial",
            "numero_receptor",
            "direccion",
            "provincia",
            "localidad",
            "codigo_postal",
            "numero_administracion",
        ]


########################################
############### REGISTER ###############
########################################


class UsuarioRegisterSerializer(serializers.ModelSerializer):
    # Define password fields for incoming requests
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Usuario
        fields = [
            "tipo",
            "dni",
            "nombre",
            "apellidos",
            "telefono",
            "email",
            "administracion",
            "password1",  # Include in fields to accept from frontend
            "password2",  # Include in fields to accept from frontend
        ]

    # Validate that email is unique
    def validate_email(self, value: str) -> str:
        """
        Custom validation for email to ensure it is unique.
        """
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    # Validate that DNI is unique
    def validate_dni(self, value: str) -> str:
        """
        Custom validation for DNI to ensure it is unique and within the valid format.
        """
        if Usuario.objects.filter(dni=value).exists():
            raise serializers.ValidationError("This DNI is already in use.")
        # if not re.match(r"^\d{7,10}$", value):
        if len(value) != 9:
            raise serializers.ValidationError("DNI must be with 9 digits.")
        return value

    # Validate that phone number has a correct format (e.g. numeric, valid length)
    def validate_telefono(self, value: str) -> str:
        """
        Custom validation for phone number format.
        """
        if not re.match(r"^\+?\d{8,12}$", value):
            raise serializers.ValidationError("Phone number must be between 8 and 12 digits.")
        return value

    # Validate that passwords match
    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cross-field validation for passwords and 'apellidos' based on 'tipo'.
        """
        # Validate apellidos based on tipo
        if data.get("tipo") == "PF" and not data.get("apellidos"):
            raise serializers.ValidationError({"apellidos": "Apellidos is required for Persona Física."})

        if data.get("tipo") == "PJ":
            data["apellidos"] = ""

        password1 = data.get("password1")
        password2 = data.get("password2")

        if password1 != password2:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        if len(password1) < 8:
            raise serializers.ValidationError({"password": "Password must be at least 8 characters long."})

        # Extract the password from the validated data
        data["password"] = password1
        data.pop("password1")
        data.pop("password2")

        return data

    # Overriding create to handle password hashing and saving
    def create(self, validated_data: Dict[str, Any]) -> Usuario:
        """
        Overriding create method to handle password hashing and user creation.
        """
        password = validated_data.pop("password", None)
        email = validated_data.pop("email", None)

        # Use the manager to create the user with the hashed password
        user = Usuario.objects.create_usuario(email=email, password=password, **validated_data)

        return user


class AdministracionRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administracion
        fields = [
            "nombre_comercial",
            "numero_receptor",
            "direccion",
            "provincia",
            "localidad",
            "codigo_postal",
            "numero_administracion",
        ]

    # Field-level validation for numero_receptor (should be unique)
    def validate_numero_receptor(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("The numero_receptor must contain only digits.")
        if len(value) != 5:
            raise serializers.ValidationError("The numero_receptor must be exactly 5 digits long.")
        if Administracion.objects.filter(numero_receptor=value).exists():
            raise serializers.ValidationError("This numero_receptor is already in use.")
        return value

    # Field-level validation for numero_administracion (custom length or pattern validation)
    def validate_numero_administracion(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("El numero_administracion debe contener solo dígitos.")
        if len(value) > 5:
            raise serializers.ValidationError("El numero_administracion debe tener como maximo 5 dígitos.")
        return value

    # Field-level validation for provincia
    def validate_provincia(self, value):
        print(value)
        if not value:
            raise serializers.ValidationError("Provincia is a required field.")

        # Comprobar si la provincia es válida según PROVINCIAS_CHOICES
        provincias_keys = [choice[0] for choice in PROVINCIAS_CHOICES]
        if value.id not in provincias_keys:
            raise serializers.ValidationError("Provincia is not a valid value from the select form.")

        return value

    # Field-level validation for localidad
    def validate_localidad(self, value):
        if not value:
            raise serializers.ValidationError("Localidad is a required field.")
        return value

    # Field-level validation for numero_administracion (custom length or pattern validation)
    def validate_codigo_postal(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("El codigo_postal debe contener solo dígitos.")
        if len(value) != 5:
            raise serializers.ValidationError("El codigo_postal 5 dígitos.")

        return value

    # Field-level validation for direccion
    def validate_direccion(self, value):
        if not value:
            raise serializers.ValidationError("Dirección is a required field.")
        return value

    # Cross-field validation
    def validate(self, data):
        # Aquí puedes añadir validaciones que dependen de múltiples campos si es necesario
        return data

    # Overriding the create method to ensure saving logic
    def create(self, validated_data):
        return Administracion.objects.create(**validated_data)


########################################
###############  LOGIN   ###############
########################################
class UsuarioLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        # Authenticate user using email
        user = authenticate(username=email, password=password)

        if not user:  # This could also be if user IS NOT ACTIVE
            raise serializers.ValidationError(detail="Invalid form credentials.", code="AUTH_INVALID_CREDENTIALS")
        return user

    def get_tokens(self, user):
        # Generate JWT token pair (access and refresh)
        token_serializer = TokenObtainPairSerializer()
        tokens = token_serializer.get_token(user)
        return {"refresh": str(tokens), "access": str(tokens.access_token)}
