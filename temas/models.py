from django.db import models

class Temas(models.Model):
    id_tema = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    # img = models.ImageField(upload_to="temas", null=True, blank=True, default="media/fotorandom")
    img_temas = models.ImageField(upload_to='temas/',        # Carpeta dentro de MEDIA_ROOT
        null=True,
        blank=True,
        default='temas/default.png')
    informacion_tema = models.TextField()
    
    class Meta:
        managed = False
        db_table = 'temas'
# Create your models here.
