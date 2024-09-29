from django.db import models

# Create your models here.
from typing import Any, Optional

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from .constants import TIPOS_SOLICITUD

# class Solicitud(models.Model):
#     """Custom user model representing a user in the system."""

#     id = models.AutoField(primary_key=True)
#     # Tipo de usuario -> PF: Persona Fisica, PJ: Persona Juridica.
#     tipo = models.CharField(
#         max_length=2, choices=TIPOS_SOLICITUD)
#     id_administracion = models.OneToOneField(
#         "Administracion",
#         on_delete=models.CASCADE,
#         related_name="propietario",
#         null=False,
#     )

#     numero = models.CharField(max_length=10, unique=True)
#     num_series = models.CharField(max_length=50)
#     soteo = models.CharField(max_length=50, blank=True, null=True)
#     condicion = models.CharField(max_length=12)
#     num_cond = models.EmailField(max_length=254, unique=True)
#     num_series_cond = models.EmailField(max_length=254, unique=True)
#     sorteo_cond = models.EmailField(max_length=254, unique=True)
#     estado = models.EmailField(max_length=254, unique=True)
    
#     # ADITIONAL ADMON STATUS FIELDS
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


#     # Required for Django user model
#     REQUIRED_FIELDS: list[str] = [
#         "tipo",
#         "dni",
#         "nombre",
#         "telefono",
#     ]  # Fields required when creating a user

#     def __str__(self) -> str:
#         """Return a string representation of the user (DNI)."""
#         return self.id


# class Administracion(models.Model):
#     """Model representing an administration entity."""

#     id = models.AutoField(primary_key=True)
#     nombre_comercial = models.CharField(max_length=100)
#     numero_receptor = models.CharField(max_length=5, unique=True)
#     direccion = models.CharField(max_length=255)
#     provincia = models.CharField(max_length=100, choices=PROVINCIAS)
#     localidad = models.CharField(max_length=100)
#     numero_administracion = models.CharField(max_length=5)

#     def __str__(self) -> str:
#         """Return a string representation of the administration (nombre_comercial)."""
#         return self.nombre_comercial
