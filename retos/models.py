from django.db import models

class Retos(models.Model):
    id_reto = models.AutoField(primary_key=True)
    nombre_reto = models.CharField(max_length=100),
    id_tema = models.IntegerField
    descripcion = models.TextField
    pregunta = models.TextField
    img_reto = models.ImageField(upload_to='retos/',        # Carpeta dentro de MEDIA_ROOT
        null=True,
        blank=True,
        default='retos/default.png')
    recompensa_monedas = models.IntegerField
    costo_monedas = models.IntegerField
    respuesta_uno = models.CharField(max_length=100)
    respuesta_dos = models.CharField(max_length=100)
    respuesta_tres = models.CharField(max_length=100)
    respuesta_cuatro = models.CharField(max_length=100)
    respuestaCorrecta = models.CharField(max_length=100)
    
    class Meta:
        managed = False  # Django no manejará esta tabla (ya existe en MySQL)
        db_table = 'retos'
# Create your models here.
