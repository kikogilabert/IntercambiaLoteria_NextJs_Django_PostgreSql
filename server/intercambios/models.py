from django.db import models, transaction
from simple_history.models import HistoricalRecords

from intercambios.constants import (
    ESTADO_ABIERTA,
    ESTADO_ACEPTADA,
    ESTADO_CANCELADA,
    ESTADO_COMPLETADA,
    ESTADO_RECHAZADA,
    ESTADOS_RESPUESTA,
    ESTADOS_SOLICITUD,
    TIPOS_CONDICION,
    TIPOS_SOLICITUD,
)

from core.models import Sorteo, StateManager
from usuario.models import Administracion


class Solicitud(StateManager):
    """Custom model representing a Solicitud in the system."""

    id = models.AutoField(primary_key=True)
    tipo = models.IntegerField(choices=TIPOS_SOLICITUD)
    administracion = models.ForeignKey(
        Administracion, on_delete=models.CASCADE, related_name="solicitudes", null=False
    )
    numero = models.CharField(
        max_length=5
    )  # tipo='oferta': Numero exacto | tipo='busqueda': numero exacto o condicion.
    num_series = models.IntegerField()
    sorteo = models.ForeignKey(
        Sorteo, on_delete=models.CASCADE, related_name="solicitudes"
    )

    # Condicion
    condicion = models.IntegerField(choices=TIPOS_CONDICION)
    num_cond = models.CharField(max_length=5, null=True, blank=True)
    num_series_cond = models.IntegerField(null=True, blank=True)
    sorteo_cond = models.ForeignKey(
        Sorteo,
        on_delete=models.CASCADE,
        related_name="solicitudes_cond",
        null=True,
        blank=True,
    )

    # Estado
    estado = models.CharField(
        max_length=20, default=ESTADO_ABIERTA, choices=ESTADOS_SOLICITUD
    )

    # Add historical record of changes.
    history = HistoricalRecords()
    # Datatime of creation or update.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Solicitud {self.id} - {self.administracion} - Número: {self.numero} - Sorteo: {self.sorteo.codigo}"


class Respuesta(StateManager):
    """Custom model representing a Respuesta in the system."""

    id = models.AutoField(primary_key=True)
    solicitud = models.ForeignKey(
        Solicitud, on_delete=models.CASCADE, related_name="respuestas"
    )
    administracion = models.ForeignKey(
        Administracion, on_delete=models.CASCADE, related_name="respuestas", null=False
    )

    numero = models.CharField(max_length=5)
    num_series = models.IntegerField()
    sorteo = models.ForeignKey(
        Sorteo, on_delete=models.CASCADE, related_name="respuestas"
    )

    estado = models.CharField(
        max_length=20, default=ESTADO_ABIERTA, choices=ESTADOS_RESPUESTA
    )

    # Add historical record of changes.
    history = HistoricalRecords()
    # Datatime of creation or update.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Respuesta {self.id} - {self.administracion} - Número: {self.numero} - Sorteo: {self.sorteo.codigo}"


class Intercambio(models.Model):
    # Keys of intercambio.
    id = models.AutoField(primary_key=True)
    solicitud = models.ForeignKey(
        Solicitud, on_delete=models.CASCADE, related_name="intercambios"
    )
    solicitud_respuesta = models.ForeignKey(
        Respuesta, on_delete=models.CASCADE, related_name="intercambios"
    )
    origen = models.ForeignKey(
        "LoteriaIntercambio",
        on_delete=models.CASCADE,
        related_name="enviadas_en_intercambio",
    )
    destino = models.ForeignKey(
        "LoteriaIntercambio",
        on_delete=models.CASCADE,
        related_name="recibidas_en_intercambio",
    )

    # Add historical record of changes.
    history = HistoricalRecords()
    # Datatime of creation or update.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Intercambio {self.id} between {self.solicitud.administracion} and {self.solicitud_respuesta.administracion}"

    def realizar_intercambio(self):
        """Método para completar un intercambio, cambiando el estado de las solicitudes involucradas."""

        with transaction.atomic():
            try:
                if (
                    self.solicitud.estado == ESTADO_ABIERTA
                    and self.solicitud_respuesta.estado == ESTADO_ACEPTADA
                ):
                    self.solicitud.completar()
                    self.solicitud_respuesta.completar()

                    # Cancelar otras respuestas vinculadas a la solicitud
                    responses_to_cancel = (
                        Respuesta.objects.filter(solicitud=self.solicitud)
                        .exclude(pk=self.solicitud_respuesta.pk)
                        .exclude(
                            estado__in=[
                                ESTADO_COMPLETADA,
                                ESTADO_CANCELADA,
                                ESTADO_RECHAZADA,
                            ]
                        )
                    )

                    for respuesta in responses_to_cancel:
                        respuesta.cancelar()

                    return True
                return False
            except ValueError:
                # Handle exception or log error
                return False


class LoteriaIntercambio(models.Model):
    administracion = models.ForeignKey(Administracion, on_delete=models.CASCADE)
    numero = models.CharField(max_length=5)
    num_series = models.IntegerField()
    sorteo = models.ForeignKey(
        Sorteo, on_delete=models.CASCADE, related_name="loteria_intercambio"
    )

    def __str__(self):
        return f"Loteria {self.numero} con {self.num_series} series en el sorteo {self.sorteo}"
