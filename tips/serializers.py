from rest_framework import serializers


class TipPeriodicaCreateUpdateSerializer(serializers.Serializer):
    id_perfil = serializers.IntegerField(required=False, allow_null=True, default=None)
    nombre = serializers.CharField(max_length=100)
    descripcion = serializers.CharField()


class TipPeriodicaSerializer(serializers.Serializer):
    id_recompensa = serializers.IntegerField()
    id_perfil = serializers.IntegerField()
    nombre = serializers.CharField(max_length=100)
    descripcion = serializers.CharField()
