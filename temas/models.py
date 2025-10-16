from django.db import models

class Temas(models.Model):
    id_tema = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio  = models.IntegerField(default=0)
    
    class Meta:
        managed = False
        db_table = 'temas'
# Create your models here.
