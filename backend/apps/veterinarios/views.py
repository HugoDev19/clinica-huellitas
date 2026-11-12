from drf_spectacular.utils import extend_schema
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


class VeterinarioDetailView(APIView):
    @extend_schema(responses=VeterinarioSerializer)
    def get(self, request, veterinario_id):
        servicio = construir_servicio_veterinarios()
        veterinario = servicio.obtener(veterinario_id)
        return Response(VeterinarioSerializer(veterinario).data)
