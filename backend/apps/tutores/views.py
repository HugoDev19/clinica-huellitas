from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from application.dto import RegistrarTutorDTO
from infrastructure.container import construir_servicio_tutores_mascotas

from .serializers import TutorSerializer


class TutorListCreateView(APIView):
    pagination_class = PageNumberPagination

    @extend_schema(responses=TutorSerializer(many=True))
    def get(self, request):
        servicio = construir_servicio_tutores_mascotas()
        tutores = servicio.listar_tutores()
        paginador = self.pagination_class()
        pagina = paginador.paginate_queryset(tutores, request, view=self)
        return paginador.get_paginated_response(TutorSerializer(pagina, many=True).data)

    @extend_schema(request=TutorSerializer, responses=TutorSerializer)
    def post(self, request):
        serializer = TutorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        servicio = construir_servicio_tutores_mascotas()
        dto = RegistrarTutorDTO(**serializer.validated_data)
        tutor = servicio.registrar_tutor(dto)
        return Response(TutorSerializer(tutor).data, status=status.HTTP_201_CREATED)
