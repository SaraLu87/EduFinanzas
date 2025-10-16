from rest_framework import serializers

class RetoSerializer(serializers.Serializer):
    id_reto = serializers.IntegerField(read_only=True)
    tipo_pregunta = serializers.CharField(max_length=50)
    nombre_reto = serializers.CharField(max_length=100)
    id_tema = serializers.IntegerField()
    descripcion = serializers.CharField()
    recompensa_monedas = serializers.IntegerField()
    respuesta_uno = serializers.CharField(allow_blank=True, required=False)
    respuesta_dos = serializers.CharField(allow_blank=True, required=False)
    respuesta_tres = serializers.CharField(allow_blank=True, required=False)
    respuesta_cuatro = serializers.CharField(allow_blank=True, required=False)
    respuestaCorrecta = serializers.CharField(max_length=100)

class RetoCreateUpdateSerializer(serializers.Serializer):
    tipo_pregunta = serializers.CharField(max_length=50)
    nombre_reto = serializers.CharField(max_length=100)
    id_tema = serializers.IntegerField()
    descripcion = serializers.CharField()
    recompensa_monedas = serializers.IntegerField()
    respuesta_uno = serializers.CharField(allow_blank=True, required=False)
    respuesta_dos = serializers.CharField(allow_blank=True, required=False)
    respuesta_tres = serializers.CharField(allow_blank=True, required=False)
    respuesta_cuatro = serializers.CharField(allow_blank=True, required=False)
    respuestaCorrecta = serializers.CharField(max_length=100)
