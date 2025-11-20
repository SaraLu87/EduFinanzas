from rest_framework import serializers

class TemaCreateUpdateSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=100)
    descripcion = serializers.CharField()  # TextField se representa como CharField en serializers
    img_tema = serializers.ImageField(required=False, allow_null=True, default=None)
    informacion_tema = serializers.CharField()

class TemaSerializer(serializers.Serializer):
    id_tema = serializers.IntegerField()
    nombre = serializers.CharField(max_length=100)
    descripcion = serializers.CharField()
    img_tema = serializers.ImageField(required=False, allow_null=True, default=None)
    informacion_tema = serializers.CharField()