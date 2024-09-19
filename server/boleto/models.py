from django.db import models

# Create your models here.

class Boleto(models.Model):
    id = models.AutoField(primary_key=True)
    numero_boleto = models.IntegerField() # numero de boleto XXXXX
    series_boleto = models.JSONField(null=True, blank=True) # serie de boleto XXXX
    num_series_disponibles = models.IntegerField() # series disponibles para intercambiar
    administracion = models.ForeignKey('administracion.Administracion', on_delete=models.CASCADE) # administracion en la que se encuentra el boleto