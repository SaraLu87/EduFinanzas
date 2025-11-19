from rest_framework import serializers

class PerfilCreateSerializer(serializers.Serializer):
    id_usuario = serializers.IntegerField()
    nombre_perfil = serializers.CharField(max_length=50)
    edad = serializers.IntegerField()
    #monedas = serializers.IntegerField(default=0, min_value=0)
    # Ahora es ImageField para subir archivos
    foto_perfil = serializers.ImageField(
        required=False,
        allow_null=True,
        default = None
    )

class PerfilUpdateSerializer(serializers.Serializer):
    nombre_perfil = serializers.CharField(max_length=50)
    edad = serializers.IntegerField()
    #monedas = serializers.IntegerField(default=0, min_value=0)
    # Ahora es ImageField para subir archivos
    foto_perfil = serializers.ImageField(
        required=False,
        allow_null=True,
        default = None
    )

class PerfilSerializer(serializers.Serializer):
    id_perfil = serializers.IntegerField()
    id_usuario = serializers.IntegerField()
    nombre_perfil = serializers.CharField(max_length=50)
    edad = serializers.IntegerField()
    # Este devolverá la URL pública: http://localhost:8000/media/perfiles/imagen.png
    foto_perfil = serializers.ImageField(
        required=False,
        allow_null=True,
        default = None
    )