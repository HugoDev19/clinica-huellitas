from collections import Counter
from datetime import date

from django.utils import timezone
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from application.dto import AgendarCitaDTO, AtenderCitaDTO
from domain.enums import EstadoCita, TipoConsulta
from domain.ports import FiltrosCitas
from infrastructure.container import construir_servicio_citas

from .serializers import AtenderCitaSerializer, CitaSerializer, DashboardSerializer


def _parse_date(valor):
    if not valor:
        return None
    try:
        return date.fromisoformat(valor)
    except ValueError as exc:
        raise ValidationError({"fecha": "Usa el formato YYYY-MM-DD."}) from exc


def _parse_int(valor):
    if not valor:
        return None
    try:
        return int(valor)
    except ValueError as exc:
        raise ValidationError({"id": "Debe ser un número entero."}) from exc


class CitaListCreateView(APIView):
    pagination_class = PageNumberPagination

    @extend_schema(
        responses=CitaSerializer(many=True),
        parameters=[
            OpenApiParameter("fecha", str, description="Filtrar por fecha (YYYY-MM-DD)"),
            OpenApiParameter("veterinario_id", int),
            OpenApiParameter("mascota_id", int),
            OpenApiParameter("estado", str),
        ],
    )
    def get(self, request):
        filtros = FiltrosCitas(
            fecha=_parse_date(request.query_params.get("fecha")),
            veterinario_id=_parse_int(request.query_params.get("veterinario_id")),
            mascota_id=_parse_int(request.query_params.get("mascota_id")),
            estado=request.query_params.get("estado"),
        )
        servicio = construir_servicio_citas()
        citas = servicio.listar_citas(filtros)
        paginador = self.pagination_class()
        pagina = paginador.paginate_queryset(citas, request, view=self)
        return paginador.get_paginated_response(CitaSerializer(pagina, many=True).data)

    @extend_schema(request=CitaSerializer, responses=CitaSerializer)
    def post(self, request):
        serializer = CitaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        datos = serializer.validated_data
        dto = AgendarCitaDTO(
            mascota_id=datos["mascota_id"],
            veterinario_id=datos["veterinario_id"],
            fecha_hora=datos["fecha_hora"],
            tipo_consulta=TipoConsulta(datos["tipo_consulta"]),
            observaciones=datos.get("observaciones", ""),
        )
        servicio = construir_servicio_citas()
        cita = servicio.agendar_cita(dto)
        return Response(CitaSerializer(cita).data, status=status.HTTP_201_CREATED)


class CitaDetailView(APIView):
    @extend_schema(responses=CitaSerializer)
    def get(self, request, cita_id):
        servicio = construir_servicio_citas()
        cita = servicio.obtener_cita(cita_id)
        return Response(CitaSerializer(cita).data)


class AgendaDiariaView(APIView):
    @extend_schema(
        responses=CitaSerializer(many=True),
        parameters=[
            OpenApiParameter("veterinario_id", int, required=True),
            OpenApiParameter("fecha", str, required=True, description="YYYY-MM-DD"),
        ],
    )
    def get(self, request):
        veterinario_id = request.query_params.get("veterinario_id")
        fecha_str = request.query_params.get("fecha")
        if not veterinario_id or not fecha_str:
            return Response(
                {
                    "error": "PARAMETROS_REQUERIDOS",
                    "detalle": "veterinario_id y fecha son requeridos",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        servicio = construir_servicio_citas()
        veterinario_id = _parse_int(veterinario_id)
        fecha = _parse_date(fecha_str)
        citas = servicio.consultar_agenda_diaria(veterinario_id, fecha)
        return Response(CitaSerializer(citas, many=True).data)


class CancelarCitaView(APIView):
    @extend_schema(request=None, responses=CitaSerializer)
    def post(self, request, cita_id):
        servicio = construir_servicio_citas()
        cita = servicio.cancelar_cita(cita_id)
        return Response(CitaSerializer(cita).data)


class AtenderCitaView(APIView):
    @extend_schema(request=AtenderCitaSerializer, responses=CitaSerializer)
    def post(self, request, cita_id):
        serializer = AtenderCitaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        servicio = construir_servicio_citas()
        dto = AtenderCitaDTO(cita_id=cita_id, observaciones=serializer.validated_data.get("observaciones", ""))
        cita = servicio.atender_cita(dto)
        return Response(CitaSerializer(cita).data)


class NoAsistioCitaView(APIView):
    @extend_schema(request=None, responses=CitaSerializer)
    def post(self, request, cita_id):
        servicio = construir_servicio_citas()
        cita = servicio.marcar_no_asistio(cita_id)
        return Response(CitaSerializer(cita).data)


class DashboardView(APIView):
    @extend_schema(
        responses=DashboardSerializer,
        parameters=[OpenApiParameter("fecha", str, description="YYYY-MM-DD, por defecto hoy")],
    )
    def get(self, request):
        fecha_str = request.query_params.get("fecha")
        fecha = _parse_date(fecha_str) if fecha_str else timezone.localdate()

        servicio = construir_servicio_citas()
        citas_del_dia = servicio.listar_citas(FiltrosCitas(fecha=fecha))

        por_estado = Counter(c.estado.value for c in citas_del_dia)
        por_veterinario = Counter(c.veterinario_id for c in citas_del_dia)
        proximas = sorted(
            (c for c in citas_del_dia if c.estado == EstadoCita.PROGRAMADA),
            key=lambda c: c.fecha_hora,
        )[:5]

        return Response(
            {
                "fecha": fecha.isoformat(),
                "total_citas": len(citas_del_dia),
                "programadas": por_estado.get(EstadoCita.PROGRAMADA.value, 0),
                "atendidas": por_estado.get(EstadoCita.ATENDIDA.value, 0),
                "canceladas": por_estado.get(EstadoCita.CANCELADA.value, 0),
                "no_asistio": por_estado.get(EstadoCita.NO_ASISTIO.value, 0),
                "proximas_citas": CitaSerializer(proximas, many=True).data,
                "distribucion_por_veterinario": [
                    {"veterinario_id": vet_id, "total": total}
                    for vet_id, total in por_veterinario.items()
                ],
            }
        )
