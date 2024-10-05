import re
from typing import Any, Dict

from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .constants import PROVINCIAS_CHOICES
from .models import Administracion  # Assuming your models are in models.py
from .models import Usuario


class ProfileGetSerializer(serializers.ModelSerializer):
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
        ]


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            "tipo",
            "dni",
            "nombre",
            "apellidos",
            "telefono",
            "email",
            "password",
        ]


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            "id",
            "tipo",
            "dni",
            "nombre",
            "apellidos",
            "telefono",
            "email",
            "administracion",
            "password",
        ]


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
            raise serializers.ValidationError(
                "Phone number must be between 8 and 12 digits."
            )
        return value

    # Validate that passwords match
    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cross-field validation for passwords and 'apellidos' based on 'tipo'.
        """
        # Validate apellidos based on tipo
        if data.get("tipo") == "PF" and not data.get("apellidos"):
            raise serializers.ValidationError(
                {"apellidos": "Apellidos is required for Persona Física."}
            )

        if data.get("tipo") == "PJ":
            data["apellidos"] = ""

        password1 = data.get("password1")
        password2 = data.get("password2")

        if password1 != password2:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        if len(password1) < 8:
            raise serializers.ValidationError(
                {"password": "Password must be at least 8 characters long."}
            )

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
        user = Usuario.objects.create_usuario(
            email=email, password=password, **validated_data
        )

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
            "numero_administracion",
        ]


class AdministracionRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administracion
        fields = [
            "nombre_comercial",
            "numero_receptor",
            "direccion",
            "provincia",
            "localidad",
            "numero_administracion",
        ]

    # Field-level validation for numero_receptor (should be unique)
    def validate_numero_receptor(self, value):
        if not value.isdigit():
            raise serializers.ValidationError(
                "The numero_receptor must contain only digits."
            )
        if len(value) != 5:
            raise serializers.ValidationError(
                "The numero_receptor must be exactly 5 digits long."
            )
        if Administracion.objects.filter(numero_receptor=value).exists():
            raise serializers.ValidationError("This numero_receptor is already in use.")
        return value

    # Field-level validation for numero_administracion (custom length or pattern validation)
    def validate_numero_administracion(self, value):
        if not value.isdigit():
            raise serializers.ValidationError(
                "El numero_administracion debe contener solo dígitos."
            )
        if len(value) > 5:
            raise serializers.ValidationError(
                "El numero_administracion debe tener como maximo 5 dígitos."
            )

        return value

    # Cross-field validation
    def validate(self, data):
        # Example of validating a combination of fields
        provincia = data.get("provincia")
        localidad = data.get("localidad")
        direccion = data.get("direccion")

        if not provincia:
            raise serializers.ValidationError(
                {"provincia": " Provincia is a required field."}
            )

        provincias_keys = [choice[0] for choice in PROVINCIAS_CHOICES]
        if provincia not in provincias_keys:
            raise serializers.ValidationError(
                {"provincia": " Provincia is not a valid value from select form."}
            )

        if not localidad:
            raise serializers.ValidationError(
                {"localidad": " Localidad is required field."}
            )

        if not direccion:
            raise serializers.ValidationError(
                {"direccion": " Dirección is required field."}
            )

        return data

    # Overriding the create method to ensure saving logic
    def create(self, validated_data):
        return Administracion.objects.create(**validated_data)



# from django.contrib.auth.models import User

# Get the custom user model
User = get_user_model()


class UsuarioLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        # Authenticate user using email
        user = authenticate(username=email, password=password)

        if not user: #This could also be if user IS NOT ACTIVE
            raise serializers.ValidationError(detail="Invalid form credentials.", code="AUTH_INVALID_CREDENTIALS")
        return user

    def get_tokens(self, user):
        # Generate JWT token pair (access and refresh)
        token_serializer = TokenObtainPairSerializer()
        tokens = token_serializer.get_token(user)
        return {"refresh": str(tokens), "access": str(tokens.access_token)}
