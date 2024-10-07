from django.db import models, transaction

from core.exceptions import InvalidStateTransition


class Pais(models.Model):
    nombre = models.CharField(max_length=100)
    nombre_front = models.CharField(max_length=100)
    codigo = models.CharField(max_length=2, unique=True)  # Código ISO del país, por ejemplo 'ES' para España

    def __str__(self):
        return self.nombre


class ComunidadAutonoma(models.Model):
    nombre = models.CharField(max_length=100)
    nombre_front = models.CharField(max_length=100)
    codigo = models.CharField(max_length=2, unique=True)  # Código de cada comunidad autónoma
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name="comunidades_autonomas")

    def __str__(self):
        return self.nombre


class Provincia(models.Model):
    nombre = models.CharField(max_length=100)
    nombre_front = models.CharField(max_length=100)
    codigo = models.CharField(max_length=2, unique=True)  # Código de cada provincia
    comunidad_autonoma = models.ForeignKey(
        ComunidadAutonoma, null=True, blank=True, on_delete=models.CASCADE, related_name="provincias"
    )
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name="provincias")


    def __str__(self):
        return self.nombre


class Sorteo(models.Model):
    codigo = models.CharField(
        max_length=6, unique=True
    )  # Código del sorteo, con longitud máxima de 6 NNN/AA.
    fecha = models.DateField()  # Fecha del sorteo
    precio = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Precio con hasta 10 dígitos y 2 decimales

    def __str__(self):
        return f"Sorteo {self.codigo} - Fecha: {self.fecha} - Precio: {self.precio}"


class StateManager(models.Model):
    """Clase base abstracta para proporcionar métodos comunes de gestión de estados a los modelos."""

    estado = models.CharField(max_length=20)

    @transaction.atomic
    def change_state(self, new_state, valid_current_states):
        if self.estado not in valid_current_states:
            raise InvalidStateTransition(f"No se puede cambiar el estado de {self.estado} a {new_state}.")
        self.estado = new_state
        self.save()
        # Devolvemos una respuesta de éxito con el estado actualizado
        return f"El estado ha sido cambiado exitosamente a {self.estado}."

    class Meta:
        abstract = True
