"""Patron State: encapsula las transiciones permitidas de una Cita (RN8).

Cada estado sabe a que estados puede moverse y bajo que condiciones.
La entidad Cita delega en el handler correspondiente en vez de usar
condicionales dispersos por el codigo.
"""
from abc import ABC
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from domain.enums import EstadoCita
from domain.exceptions import CancelacionNoPermitidaError, TransicionEstadoInvalidaError

if TYPE_CHECKING:
    from domain.entities import Cita

HORAS_MINIMAS_CANCELACION = 2


class EstadoCitaHandler(ABC):
    estado: EstadoCita

    def cancelar(self, cita: "Cita", ahora: datetime) -> None:
        raise TransicionEstadoInvalidaError(
            f"No se puede cancelar una cita en estado {self.estado.value}"
        )

    def atender(self, cita: "Cita", observaciones: str = "") -> None:
        raise TransicionEstadoInvalidaError(
            f"No se puede atender una cita en estado {self.estado.value}"
        )

    def marcar_no_asistio(self, cita: "Cita") -> None:
        raise TransicionEstadoInvalidaError(
            f"No se puede marcar inasistencia en una cita en estado {self.estado.value}"
        )


class ProgramadaState(EstadoCitaHandler):
    estado = EstadoCita.PROGRAMADA

    def cancelar(self, cita: "Cita", ahora: datetime) -> None:
        limite = cita.fecha_hora - timedelta(hours=HORAS_MINIMAS_CANCELACION)
        if ahora > limite:
            raise CancelacionNoPermitidaError(
                "Solo se puede cancelar con al menos dos horas de anticipacion"
            )
        cita.estado = EstadoCita.CANCELADA

    def atender(self, cita: "Cita", observaciones: str = "") -> None:
        cita.estado = EstadoCita.ATENDIDA
        cita.observaciones = observaciones

    def marcar_no_asistio(self, cita: "Cita") -> None:
        cita.estado = EstadoCita.NO_ASISTIO


class AtendidaState(EstadoCitaHandler):
    estado = EstadoCita.ATENDIDA


class CanceladaState(EstadoCitaHandler):
    estado = EstadoCita.CANCELADA


class NoAsistioState(EstadoCitaHandler):
    estado = EstadoCita.NO_ASISTIO


_ESTADOS = {
    EstadoCita.PROGRAMADA: ProgramadaState(),
    EstadoCita.ATENDIDA: AtendidaState(),
    EstadoCita.CANCELADA: CanceladaState(),
    EstadoCita.NO_ASISTIO: NoAsistioState(),
}


def obtener_estado(estado: EstadoCita) -> EstadoCitaHandler:
    return _ESTADOS[estado]
