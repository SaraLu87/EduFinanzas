from rest_framework import serializers

class PerfilCreateUpdateSerializer(serializers.Serializer):
    id_usuario = serializers.IntegerField()
    nombre_perfil = serializers.CharField(max_length=50)
    foto_perfil = serializers.CharField(max_length=255, default='default.png')
    tema_actual = serializers.IntegerField(default=1)
    monedas = serializers.IntegerField(default=0, min_value=0)


class PerfilSerializer(serializers.Serializer):
    id_perfil = serializers.IntegerField()
    id_usuario = serializers.IntegerField()
    nombre_perfil = serializers.CharField(max_length=50)
    foto_perfil = serializers.CharField(max_length=255)
    tema_actual = serializers.IntegerField()
    monedas = serializers.IntegerField()
