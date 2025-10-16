from django.db import models

class Perfiles(models.Model):
    id_perfil = models.AutoField(primary_key=True)
    id_usuario = models.IntegerField()  # Llave foránea a usuarios (sin relación directa por managed=False)
    nombre_perfil = models.CharField(max_length=50, unique=True)
    foto_perfil = models.CharField(max_length=255, default='default.png')
    tema_actual = models.IntegerField(default=1)
    monedas = models.IntegerField(default=0)

    class Meta:
        managed = False  # Django no creará ni modificará esta tabla
        db_table = 'perfiles'
