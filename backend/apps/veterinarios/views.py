from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from infrastructure.container import construir_servicio_veterinarios

from .serializers import VeterinarioSerializer


class VeterinarioListView(APIView):
    @extend_schema(responses=VeterinarioSerializer(many=True))
    def get(self, request):
        servicio = construir_servicio_veterinarios()
        veterinarios = servicio.listar()
        return Response(VeterinarioSerializer(veterinarios, many=True).data)

    @extend_schema(request=VeterinarioSerializer, responses=VeterinarioSerializer)
    def post(self, request):
        serializer = VeterinarioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        servicio = construir_servicio_veterinarios()
        veterinario = servicio.registrar(
            codigo=serializer.validated_data["codigo"],
            nombre=serializer.validated_data["nombre"],
        )
        return Response(
            VeterinarioSerializer(veterinario).data,
            status=status.HTTP_201_CREATED,
        )


class VeterinarioDetailView(APIView):
    @extend_schema(responses=VeterinarioSerializer)
    def get(self, request, veterinario_id):
        servicio = construir_servicio_veterinarios()
        veterinario = servicio.obtener(veterinario_id)
        return Response(VeterinarioSerializer(veterinario).data)
