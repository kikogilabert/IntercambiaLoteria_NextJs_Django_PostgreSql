from django.db import models

class Pais(models.Model):
    nombre = models.CharField(max_length=100, unique=True)  # Country name
    codigo_iso = models.CharField(max_length=2, unique=True)  # Optional ISO code for the country

    def __str__(self):
        return self.nombre


class ComunidadAutonoma(models.Model):
    nombre = models.CharField(max_length=100, unique=True)  # Autonomous Community name
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name='comunidades')

    def __str__(self):
        return self.nombre


class Provincia(models.Model):
    nombre = models.CharField(max_length=100)  # Province name
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name="provincias")
    comunidad = models.ForeignKey(
        ComunidadAutonoma, on_delete=models.SET_NULL, null=True, blank=True, related_name="provincias"
    )  # Optional, can be null for countries without autonomous communities.
    short_code = models.CharField(max_length=50, blank=True, null=True)  # Optional short code

    class Meta:
        unique_together = ('nombre', 'pais')  # Ensure unique provinces per country

    def __str__(self):
        return f"{self.nombre} ({self.pais.nombre})"