from django.db import models


class Pais(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=2, unique=True)  # Código ISO del país, por ejemplo 'ES' para España

    def __str__(self):
        return self.nombre


class ComunidadAutonoma(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=2, unique=True)  # Código de cada comunidad autónoma
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name='comunidades_autonomas')

    def __str__(self):
        return self.nombre


class Provincia(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=2, unique=True)  # Código de cada provincia
    comunidad_autonoma = models.ForeignKey(
        ComunidadAutonoma, null=True, blank=True, on_delete=models.CASCADE, related_name='provincias'
    )
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name='provincias')


    def __str__(self):
        return self.nombre
