from django.db import models

class TipsPeriodicas(models.Model):
    id_recompensa = models.AutoField(primary_key=True)
    id_perfil = models.IntegerField()
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    class Meta:
        managed = False  # Django no manejará esta tabla (ya existe en MySQL)
        db_table = 'tips_periodicas'
