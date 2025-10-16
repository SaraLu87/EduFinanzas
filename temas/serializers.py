from rest_framework import serializers

class TemaCreateUpdateSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=100)
    descripcion = serializers.CharField()  # TextField se representa como CharField en serializers
    precio = serializers.IntegerField(default=0, min_value=0)


class TemaSerializer(serializers.Serializer):
    id_tema = serializers.IntegerField()
    nombre = serializers.CharField(max_length=100)
    descripcion = serializers.CharField()
    precio = serializers.IntegerField()