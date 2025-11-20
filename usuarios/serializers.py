from rest_framework import serializers

class UsuarioCreateUpdateSerializer(serializers.Serializer):
    correo = serializers.CharField(max_length=100)
    contrasena = serializers.CharField(max_length=255, required=False, allow_blank=True)
    rol = serializers.ChoiceField(choices=['Usuario', 'Administrador'], default='Usuario')


class UsuarioSerializer(serializers.Serializer):
    id_usuario = serializers.IntegerField()
    correo = serializers.CharField(max_length=100)
    contrasena = serializers.CharField(max_length=255)
    rol = serializers.CharField(max_length=20)
    fecha_registro = serializers.DateTimeField()
