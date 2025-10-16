from rest_framework import serializers

class ProgresoCreateUpdateSerializer(serializers.Serializer):
    id_perfil = serializers.IntegerField()
    id_reto = serializers.IntegerField()
    completado = serializers.BooleanField(default=False)
    fecha_completado = serializers.DateTimeField(required=False, allow_null=True)
    respuesta_seleccionada = serializers.CharField(max_length=100, required=False, allow_blank=True)


class ProgresoSerializer(serializers.Serializer):
    id_progreso = serializers.IntegerField()
    id_perfil = serializers.IntegerField()
    id_reto = serializers.IntegerField()
    completado = serializers.BooleanField()
    fecha_completado = serializers.DateTimeField(allow_null=True)
    respuesta_seleccionada = serializers.CharField(max_length=100, allow_blank=True)
