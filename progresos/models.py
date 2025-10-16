from django.db import models

class Progreso(models.Model):
    id_progreso = models.AutoField(primary_key=True)
    id_perfil = models.IntegerField()
    id_reto = models.IntegerField()
    completado = models.BooleanField(default=False)
    fecha_completado = models.DateTimeField(null=True, blank=True)
    respuesta_seleccionada = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'progreso'

