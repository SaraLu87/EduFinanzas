from django.db import models

class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    correo = models.CharField(max_length=100, unique=True)
    contrasena = models.CharField(max_length=255)
    rol = models.CharField(
        max_length=20,
        choices=[('Usuario', 'Usuario'), ('Administrador', 'Administrador')],
        default='Usuario'
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'usuarios'

# Create your models here.
