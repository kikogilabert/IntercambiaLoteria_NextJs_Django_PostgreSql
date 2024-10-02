from django.db import models
from django_fsm import FSMField, transition
from usuario.models import Administracion

from .constants import (ESTADO_RESPUESTA, ESTADO_SOLICITUD, TIPOS_CONDICION,
                        TIPOS_SOLICITUD)


class Sorteo(models.Model):
    codigo = models.CharField(
        max_length=10, unique=True
    )  # Código del sorteo, con longitud máxima de 10
    fecha = models.DateField()  # Fecha del sorteo
    precio = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Precio con hasta 10 dígitos y 2 decimales

    def __str__(self):
        return f"Sorteo {self.codigo} - Fecha: {self.fecha} - Precio: {self.precio}"


class Solicitud(models.Model):
    """Custom model representing a Solicitud in the system."""

    id = models.AutoField(primary_key=True)
    tipo = models.IntegerField(choices=TIPOS_SOLICITUD)
    administracion = models.ForeignKey(
        Administracion, on_delete=models.CASCADE, related_name="solicitudes", null=False
    )
    numero = models.CharField(
        max_length=5
    )  # tipo='enviar': Numero exacto | tipo='recibir': numero exacto o condicion.
    num_series = models.CharField(max_length=3)
    sorteo = models.ForeignKey(
        Sorteo, on_delete=models.CASCADE, related_name="solicitudes"
    )

    # Condicion
    condicion = models.IntegerField(choices=TIPOS_CONDICION)
    num_cond = models.CharField(max_length=5, null=True, blank=True)
    num_series_cond = models.CharField(max_length=3, null=True, blank=True)
    sorteo_cond = models.ForeignKey(
        Sorteo,
        on_delete=models.CASCADE,
        related_name="solicitudes_cond",
        null=True,
        blank=True,
    )

    # ADITIONAL ADMON STATUS FIELDS
    estado = FSMField(default="abierta", choices=ESTADO_SOLICITUD)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Solicitud {self.id} - {self.administracion} - Número: {self.numero} - Sorteo: {self.sorteo.codigo}"

    @transition(field=estado, source="abierta", target="aceptada")
    def aceptar(self):
        """Aceptar la solicitud."""
        # Aquí puedes agregar lógica adicional si es necesario
        pass

    @transition(field=estado, source="aceptada", target="completada")
    def completar(self):
        """Completar la solicitud después del intercambio."""
        pass

    @transition(field=estado, source="*", target="cancelada")
    def cancelar(self):
        """Cancelar la solicitud en cualquier estado."""
        pass


class SolicitudRespuesta(models.Model):
    """Custom model representing a SolicitudRespuesta in the system."""

    id = models.AutoField(primary_key=True)
    solicitud = models.ForeignKey(
        Solicitud, on_delete=models.CASCADE, related_name="respuestas"
    )
    administracion = models.ForeignKey(
        Administracion, on_delete=models.CASCADE, related_name="respuestas", null=False
    )

    numero = models.CharField(max_length=5)
    num_series = models.CharField(max_length=3)
    sorteo = models.ForeignKey(
        Sorteo, on_delete=models.CASCADE, related_name="respuestas"
    )

    estado = FSMField(default="abierta", choices=ESTADO_RESPUESTA)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"SolicitudRespuesta {self.id} - {self.administracion} - Número: {self.numero} - Sorteo: {self.sorteo.codigo}"

    @transition(field=estado, source="pendiente", target="aceptada")
    def aceptar(self):
        """Aceptar la solicitud respuesta."""
        pass

    @transition(field=estado, source="aceptada", target="completada")
    def completar(self):
        """Completar la solicitud respuesta cuando el intercambio esté hecho."""
        pass

    @transition(field=estado, source="pendiente", target="rechazada")
    def rechazar(self):
        """Rechazar una solicitud respuesta ya aceptada."""
        pass

    @transition(field=estado, source="*", target="cancelada")
    def cancelar(self):
        """Cancelar la solicitud respuesta en cualquier estado."""
        pass


class Intercambio(models.Model):
    # Keys of intercambio.
    id = models.AutoField(primary_key=True)
    solicitud = models.ForeignKey(
        Solicitud, on_delete=models.CASCADE, related_name="intercambios"
    )
    solicitud_respuesta = models.ForeignKey(
        SolicitudRespuesta, on_delete=models.CASCADE, related_name="intercambios"
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

    # Date
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Intercambio {self.id} between {self.solicitud.administracion} and {self.solicitud_respuesta.administracion}"

    def realizar_intercambio(self):
        """Método para completar un intercambio, cambiando el estado de las solicitudes involucradas."""
        if (
            self.solicitud.estado == "aceptada"
            and self.solicitud_respuesta.estado == "aceptada"
        ):
            self.solicitud.completar()
            self.solicitud.save()
            self.solicitud_respuesta.completar()
            self.solicitud_respuesta.save()

            # Cancelar otras respuestas vinculadas a la solicitud
            otras_respuestas = SolicitudRespuesta.objects.filter(
                solicitud=self.solicitud
            ).exclude(pk=self.solicitud_respuesta.pk)

            for respuesta in otras_respuestas:
                if respuesta.estado not in ["completada", "cancelada", "rechazada"]:
                    respuesta.cancelar()
                    respuesta.save()

            # SolicitudRespuesta.objects.filter(
            #     solicitud=self.solicitud
            # ).exclude(pk=self.solicitud_respuesta.pk).exclude(
            #     estado__in=['completada', 'cancelada', 'rechazada']
            # ).update(estado='cancelada')

            return True
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
