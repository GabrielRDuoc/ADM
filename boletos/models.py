

from django.db import models

class Viaje(models.Model):
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    fecha = models.DateField()
    cantidad_de_pasajeros_disponibles = models.IntegerField()

class Ticket(models.Model):
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE)
    cantidad_de_pasajeros = models.IntegerField()

class Oferta (models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    inicio = models.DateTimeField()
    fin = models.DateTimeField()