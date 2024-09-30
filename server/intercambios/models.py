from django.db import models

from .constants import TIPOS_SOLICITUD, TIPOS_CONDICION, ESTADO_SOLICITUD, ESTADO_RESPUESTA

from ..usuario.models import Administracion

class Solicitud(models.Model):
    """Custom model representing a Solicitud in the system."""

    id = models.AutoField(primary_key=True)
    tipo = models.IntegerField(choices=TIPOS_SOLICITUD)
    administracion = models.ForeignKey(Administracion, on_delete=models.CASCADE, related_name='solicitudes', null=False)
    numero = models.CharField(max_length=5)
    num_series = models.CharField(max_length=3)
    sorteo = models.CharField(max_length=3)

    # Condicion
    #condicion = models.JSONField()
    condicion = models.IntegerField(choices=TIPOS_CONDICION)
    num_cond = models.CharField(max_length=5)
    num_series_cond = models.CharField(max_length=3)
    sorteo_cond = models.CharField(max_length=3)
    
    # ADITIONAL ADMON STATUS FIELDS
    estado = models.IntegerField(choices=ESTADO_SOLICITUD)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Required for Django user model
    REQUIRED_FIELDS: list[str] = [
        "tipo",
        "administracion",
        "numero",
        "num_series",
        "sorteo",
        "condicion",
        "num_cond",
        "num_series_cond",
        "sorteo_cond",
    ]  # Fields required when creating a user

    def __str__(self) -> str:
        """Return a id of Solicitud"""
        return str(self.id)


class SolicitudRespuesta(models.Model):
    """Custom model representing a SolicitudRespuesta in the system."""

    id = models.AutoField(primary_key=True)
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='respuestas')
    administracion = models.ForeignKey(Administracion, on_delete=models.CASCADE, related_name='respuestas', null=False)
    
    numero = models.CharField(max_length=5)
    num_series = models.CharField(max_length=3)
    sorteo = models.CharField(max_length=3)

    estado = models.IntegerField(choices=ESTADO_RESPUESTA)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    # Required for Django user model
    REQUIRED_FIELDS: list[str] = [
        "tipo",
        "solicitud",
        "administracion",
        "numero",
        "num_series",
        "sorteo",
    ]  # Fields required when creating a user

    def __str__(self) -> str:
        """Return a id of Solicitud"""
        return str(self.id)


class Intercambio(models.Model):
    # Keys of intercambio.
    id = models.AutoField(primary_key=True)
    administracion1 = models.ForeignKey(Administracion, on_delete=models.CASCADE, related_name='intercambios_enviados')
    administracion2 = models.ForeignKey(Administracion, on_delete=models.CASCADE, related_name='intercambios_recibidos')
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='intercambios')
    solicitud_respuesta = models.ForeignKey(SolicitudRespuesta, on_delete=models.CASCADE, related_name='intercambios')
    
    # Numbers
    numeros_adm1 = models.JSONField()
    numeros_adm2 = models.JSONField()

    # Date
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Intercambio {self.id} between {self.administracion1} and {self.administracion2}"
