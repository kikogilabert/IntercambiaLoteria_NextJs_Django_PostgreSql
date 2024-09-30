from typing import Any, Optional

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from .constants import PROVINCIAS, TIPOS_PERSONA, PROVINCIAS_CHOICES


class UsuarioManager(BaseUserManager):
    """Manager for Usuario model to handle user creation and retrieval."""

    def create_usuario(
        self, email: str, password: str, **extra_fields: Any
    ) -> "Usuario":
        """
        Create and return a new Usuario with an email and password.

        Args:
            email (str): The email for the user.
            password (Optional[str]): The password for the user.
            **extra_fields: Additional fields for the Usuario model.

        Returns:
            Usuario: The created user instance.
        """
        email = self.normalize_email(email)  # Normalize the email
        usuario = self.model(email=email, **extra_fields)  # Create a new user instance
        usuario.set_password(password)  # Hash the password
        usuario.save(using=self._db)  # Save the user
        return usuario

    def create_superuser(
        self, email: str, password: Optional[str] = None, **extra_fields: Any
    ) -> "Usuario":
        """
        Create and return a new superuser.

        Args:
            email (str): The email for the superuser.
            password (Optional[str]): The password for the superuser.
            **extra_fields: Additional fields for the Usuario model.

        Returns:
            Usuario: The created superuser instance.
        """
        extra_fields.setdefault("is_staff", True)  # Añadido para acceso al admin
        extra_fields.setdefault("is_superuser", True)

        return self.create_usuario(email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    """Custom user model representing a user in the system."""

    id = models.AutoField(primary_key=True)
    # Tipo de usuario -> PF: Persona Fisica, PJ: Persona Juridica.
    tipo = models.CharField(
        max_length=2, choices=TIPOS_PERSONA, default="PF"
    )  # SELECT FROM LIST
    dni = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(
        max_length=50, blank=True, null=True
    )  # EMPTY IF TIPO=PJ
    telefono = models.CharField(max_length=12)
    email = models.EmailField(max_length=254, unique=True)
    id_administracion = models.OneToOneField(
        "Administracion",
        on_delete=models.CASCADE,
        related_name="propietario",
        null=False,
    )

    # ADITIONAL ADMON STATUS FIELDS
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Permite acceso al admin panel

    objects = UsuarioManager()

    # Required for Django user model
    USERNAME_FIELD: str = "email"  # Field used for authentication
    REQUIRED_FIELDS: list[str] = [
        "tipo",
        "dni",
        "nombre",
        "telefono",
    ]  # Fields required when creating a user

    def __str__(self) -> str:
        """Return a string representation of the user (DNI)."""
        return self.email


class Administracion(models.Model):
    """Model representing an administration entity."""

    id = models.AutoField(primary_key=True)
    nombre_comercial = models.CharField(max_length=100)
    numero_receptor = models.CharField(max_length=5, unique=True)
    direccion = models.CharField(max_length=255)
    provincia = models.CharField(max_length=100, choices=PROVINCIAS_CHOICES)
    localidad = models.CharField(max_length=100)
    numero_administracion = models.CharField(max_length=5)

    def __str__(self) -> str:
        """Return a string representation of the administration (nombre_comercial)."""
        return self.nombre_comercial
