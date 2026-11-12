"""Manejo centralizado de errores: traduce excepciones de dominio a HTTP."""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from domain.exceptions import (
    CancelacionNoPermitidaError,
    DomainError,
    EntidadNoEncontradaError,
    FechaFueraDeRangoError,
    HorarioInvalidoError,
    MascotaConCitaMismoDiaError,
    MascotaConCitasError,
    TransicionEstadoInvalidaError,
    TutorDuplicadoError,
    VeterinarioDuplicadoError,
    VeterinarioNoDisponibleError,
)

_CODIGOS_HTTP = {
    EntidadNoEncontradaError: status.HTTP_404_NOT_FOUND,
    HorarioInvalidoError: status.HTTP_400_BAD_REQUEST,
    FechaFueraDeRangoError: status.HTTP_400_BAD_REQUEST,
    VeterinarioNoDisponibleError: status.HTTP_409_CONFLICT,
    MascotaConCitaMismoDiaError: status.HTTP_409_CONFLICT,
    MascotaConCitasError: status.HTTP_409_CONFLICT,
    CancelacionNoPermitidaError: status.HTTP_409_CONFLICT,
    TransicionEstadoInvalidaError: status.HTTP_409_CONFLICT,
    TutorDuplicadoError: status.HTTP_409_CONFLICT,
    VeterinarioDuplicadoError: status.HTTP_409_CONFLICT,
}


def manejador_excepciones(exc, context):
    if isinstance(exc, DomainError):
        codigo_http = status.HTTP_400_BAD_REQUEST
        for clase, codigo in _CODIGOS_HTTP.items():
            if isinstance(exc, clase):
                codigo_http = codigo
                break
        return Response({"error": exc.codigo, "detalle": str(exc)}, status=codigo_http)

    return exception_handler(exc, context)
