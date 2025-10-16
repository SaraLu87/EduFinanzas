from rest_framework import serializers

class SolucionRetoCreateSerializer(serializers.Serializer):
    id_perfil = serializers.IntegerField()
    id_reto = serializers.IntegerField()
    respuesta_seleccionada = serializers.CharField(max_length=100)


class SolucionRetoSerializer(serializers.Serializer):
    id_progreso = serializers.IntegerField(required=False)
    id_perfil = serializers.IntegerField()
    id_reto = serializers.IntegerField()
    completado = serializers.BooleanField(required=False)
    fecha_completado = serializers.DateTimeField(required=False)
    respuesta_seleccionada = serializers.CharField(max_length=100)
