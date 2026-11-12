from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from application.dto import RegistrarMascotaDTO
from infrastructure.container import construir_servicio_tutores_mascotas

from .serializers import MascotaSerializer


class MascotaListCreateView(APIView):
    pagination_class = PageNumberPagination

    @extend_schema(
        responses=MascotaSerializer(many=True),
        parameters=[OpenApiParameter("tutor_id", int, description="Filtrar por tutor")],
    )
    def get(self, request):
        tutor_id = request.query_params.get("tutor_id")
        servicio = construir_servicio_tutores_mascotas()
        mascotas = servicio.listar_mascotas(tutor_id=int(tutor_id) if tutor_id else None)
        paginador = self.pagination_class()
        pagina = paginador.paginate_queryset(mascotas, request, view=self)
        return paginador.get_paginated_response(MascotaSerializer(pagina, many=True).data)

    @extend_schema(request=MascotaSerializer, responses=MascotaSerializer)
    def post(self, request):
        serializer = MascotaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        servicio = construir_servicio_tutores_mascotas()
        dto = RegistrarMascotaDTO(**serializer.validated_data)
        mascota = servicio.registrar_mascota(dto)
        return Response(MascotaSerializer(mascota).data, status=status.HTTP_201_CREATED)


class MascotaDetailView(APIView):
    @extend_schema(responses=MascotaSerializer)
    def get(self, request, mascota_id):
        servicio = construir_servicio_tutores_mascotas()
        mascota = servicio.obtener_mascota(mascota_id)
        return Response(MascotaSerializer(mascota).data)

    @extend_schema(request=MascotaSerializer, responses=MascotaSerializer)
    def put(self, request, mascota_id):
        serializer = MascotaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        servicio = construir_servicio_tutores_mascotas()
        dto = RegistrarMascotaDTO(**serializer.validated_data)
        mascota = servicio.actualizar_mascota(mascota_id, dto)
        return Response(MascotaSerializer(mascota).data)

    @extend_schema(responses={204: None})
    def delete(self, request, mascota_id):
        servicio = construir_servicio_tutores_mascotas()
        servicio.eliminar_mascota(mascota_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
