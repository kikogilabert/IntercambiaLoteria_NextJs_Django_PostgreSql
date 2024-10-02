from django.db import models

from .constants import TIPOS_SOLICITUD, TIPOS_CONDICION, ESTADO_SOLICITUD, ESTADO_RESPUESTA

from usuario.models import Administracion

from django_fsm import FSMField, transition
from django_fsm import FSMKeyError



class Sorteo(models.Model):
    codigo = models.CharField(max_length=10, unique=True)  # Código del sorteo, con longitud máxima de 10
    fecha = models.DateField()  # Fecha del sorteo
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Precio con hasta 10 dígitos y 2 decimales

    def __str__(self):
        return f"Sorteo {self.codigo} - Fecha: {self.fecha} - Precio: {self.precio}"


class Solicitud(models.Model):
    """Custom model representing a Solicitud in the system."""

    id = models.AutoField(primary_key=True)
    tipo = models.IntegerField(choices=TIPOS_SOLICITUD)
    administracion = models.ForeignKey(Administracion, on_delete=models.CASCADE, related_name='solicitudes', null=False)
    numero = models.CharField(max_length=5) # tipo='enviar': Numero exacto | tipo='recibir': numero exacto o condicion.
    num_series = models.CharField(max_length=3)
    sorteo = models.ForeignKey(Sorteo, on_delete=models.CASCADE, related_name='solicitudes')

    # Condicion
    condicion = models.IntegerField(choices=TIPOS_CONDICION)
    num_cond = models.CharField(max_length=5, null=True, blank=True)
    num_series_cond = models.CharField(max_length=3, null=True, blank=True)
    sorteo_cond = models.ForeignKey(Sorteo, on_delete=models.CASCADE, related_name='solicitudes_cond', null=True, blank=True)
    
    # ADITIONAL ADMON STATUS FIELDS
    estado = models.IntegerField(choices=ESTADO_SOLICITUD)
    #estado = FSMField(default='abierta', choices=ESTADO_SOLICITUD)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Solicitud {self.id} - {self.administracion} - Número: {self.numero} - Sorteo: {self.sorteo.codigo}"

    @transition(field=estado, source='abierta', target='pendiente')
    def hacer_pendiente(self):
        """Cambiar el estado de 'abierta' a 'pendiente'."""
        pass

    @transition(field=estado, source='pendiente', target='aceptada')
    def aceptar_solicitud(self):
        """Aceptar la solicitud, cambiando de 'pendiente' a 'aceptada'."""
        pass

    @transition(field=estado, source='aceptada', target='completada')
    def completar_solicitud(self):
        """Completar la solicitud después de que se haya realizado el intercambio."""
        pass

    @transition(field=estado, source='*', target='cancelada')
    def cancelar_solicitud(self):
        """Cancelar la solicitud, puede ser en cualquier estado."""
        pass


class SolicitudRespuesta(models.Model):
    """Custom model representing a SolicitudRespuesta in the system."""

    id = models.AutoField(primary_key=True)
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='respuestas')
    administracion = models.ForeignKey(Administracion, on_delete=models.CASCADE, related_name='respuestas', null=False)
    
    numero = models.CharField(max_length=5)
    num_series = models.CharField(max_length=3)
    sorteo = models.ForeignKey(Sorteo, on_delete=models.CASCADE, related_name='respuestas')

    estado = models.IntegerField(choices=ESTADO_RESPUESTA)
    #estado = FSMField(default='abierta', choices=ESTADO_SOLICITUD)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"SolicitudRespuesta {self.id} - {self.administracion} - Número: {self.numero} - Sorteo: {self.sorteo.codigo}"

    @transition(field=estado, source='abierta', target='pendiente')
    def hacer_pendiente(self):
        """Cambiar el estado de 'abierta' a 'pendiente'."""
        pass

    @transition(field=estado, source='pendiente', target='aceptada')
    def aceptar_solicitud(self):
        """Aceptar la solicitud, cambiando de 'pendiente' a 'aceptada'."""
        pass

    @transition(field=estado, source='aceptada', target='completada')
    def completar_solicitud(self):
        """Completar la solicitud después de que se haya realizado el intercambio."""
        pass

    @transition(field=estado, source='*', target='cancelada')
    def cancelar_solicitud(self):
        """Cancelar la solicitud, puede ser en cualquier estado."""
        pass


class Intercambio(models.Model):
    # Keys of intercambio.
    id = models.AutoField(primary_key=True)
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='intercambios')
    solicitud_respuesta = models.ForeignKey(SolicitudRespuesta, on_delete=models.CASCADE, related_name='intercambios')
    origen = models.ForeignKey('LoteriaIntercambio', related_name='enviadas_en_intercambio')
    destino = models.ForeignKey('LoteriaIntercambio', related_name='recibidas_en_intercambio')

    # Date
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Intercambio {self.id} between {self.solicitud.administracion} and {self.solicitud_respuesta.administracion}"

    def realizar_intercambio(self):
        """Método para completar un intercambio, cambiando el estado de las solicitudes involucradas."""
        if self.solicitud.estado == 'aceptada' and self.solicitud_respuesta.estado == 'aceptada':
            self.solicitud.completar_solicitud()
            self.solicitud_respuesta.completar_respuesta()
            return True
        return False


class LoteriaIntercambio(models.Model):
    administracion = models.ForeignKey(Administracion, on_delete=models.CASCADE)
    numero = models.CharField(max_length=5)
    num_series = models.IntegerField()
    sorteo = models.ForeignKey(Sorteo, on_delete=models.CASCADE, related_name='loteria_intercambio')

    def __str__(self):
        return f"Loteria {self.numero} con {self.num_series} series en el sorteo {self.sorteo}"