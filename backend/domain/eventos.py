"""Patron Observer: eventos de agendamiento/cancelacion desacoplados de notificaciones.

El servicio de citas publica eventos sin conocer quien los consume. Los
observadores (por ejemplo, el que envia notificaciones al tutor) se suscriben
de forma independiente, cumpliendo RN9 sin acoplar ServicioCitas a un canal.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities import Cita, Mascota, Tutor


@dataclass(frozen=True)
class EventoCita:
    cita: Cita
    mascota: Mascota
    tutor: Tutor


class CitaAgendada(EventoCita):
    pass


class CitaCancelada(EventoCita):
    pass


class ObservadorEventosCita(ABC):
    @abstractmethod
    def manejar(self, evento: EventoCita) -> None:
        raise NotImplementedError


class PublicadorEventosCita:
    def __init__(self) -> None:
        self._observadores: list[ObservadorEventosCita] = []

    def suscribir(self, observador: ObservadorEventosCita) -> None:
        self._observadores.append(observador)

    def publicar(self, evento: EventoCita) -> None:
        for observador in self._observadores:
            observador.manejar(evento)
