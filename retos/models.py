from django.db import models

class retos(models.Model):
    id_reto = models.AutoField(primary_key=True)
    tipo_pregunta = models.CharField(max_length=50)
    nombre_reto = models.CharField(max_length=100),
    id_tema = models.IntegerField(models.ForeignKey("app.Model", verbose_name=_(""), on_delete=models.CASCADE))
    descripcion = models.TextField
    recompensa_monedas = models.IntegerField
    respuesta_uno = models.CharField(max_length=100)
    respuesta_dos = models.CharField(max_length=100)
    respuesta_tres = models.CharField(max_length=100)
    respuesta_cuatro = models.CharField(max_length=100)
    respuestaCorrecta = models.CharField(max_length=100)
# Create your models here.
