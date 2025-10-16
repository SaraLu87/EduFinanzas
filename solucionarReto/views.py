from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    SolucionRetoCreateSerializer,
    SolucionRetoSerializer
)
from .services import solucionar_reto_service


class SolucionRetoView(APIView):
    """
    Endpoint:
    - POST /api/solucionar_reto/  -> Ejecuta el procedimiento 'solucionar_reto'
    """

    def post(self, request):
        """Ejecutar el procedimiento para solucionar un reto"""
        serializer = SolucionRetoCreateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            resultado = solucionar_reto_service(
                data['id_perfil'],
                data['id_reto'],
                data['respuesta_seleccionada']
            )

            # Si el procedimiento devuelve datos (progreso creado o actualizado)
            if resultado:
                # Serializamos la respuesta para mantener formato uniforme
                response_serializer = SolucionRetoSerializer(resultado, many=True)
                return Response(response_serializer.data, status=status.HTTP_200_OK)

            # Si no devolvió nada (por ejemplo, la respuesta fue incorrecta)
            return Response(
                {"mensaje": "Respuesta incorrecta o sin cambios en el progreso."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Si los datos del request no son válidos
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

