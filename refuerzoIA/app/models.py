from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Imagen(models.Model):
    nombreImg = models.CharField(max_length=300)
    numRevisiones = models.IntegerField(default=0)
    inferencia = models.CharField(max_length=3500)
    maxRevisiones = models.IntegerField(default = 100)


class Revision(models.Model):
    usuario = models.ForeignKey(User, on_delete= models.SET(0))
    correcion = models.CharField(max_length=3500, null=True, blank=True)
    fechaAsignacion = models.DateTimeField(null=True, blank=True)
    fechaRevision = models.DateTimeField(null=True, blank=True)
    imagen = models.ForeignKey(Imagen,on_delete=models.CASCADE)
    tipoRevision = models.BooleanField(default=0)
    pendiente = models.BooleanField(default=1)  

    