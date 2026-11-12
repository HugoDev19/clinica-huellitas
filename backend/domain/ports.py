"""Puertos (interfaces) que el dominio y la aplicacion requieren.

Las implementaciones concretas viven en infrastructure/ y no deben filtrarse
hacia el dominio ni la aplicacion (inversion de dependencias).
"""
from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import Optional

from domain.entities import Cita, Mascota, Tutor, Veterinario


class Reloj(ABC):
    @abstractmethod
    def ahora(self) -> datetime:
        raise NotImplementedError


class UnidadDeTrabajo(ABC):
    """Delimita una transaccion atomica alrededor de un caso de uso completo.

    Permite que, por ejemplo, la lectura con bloqueo (SELECT FOR UPDATE) y la
    escritura posterior de una cancelacion de cita ocurran en una sola
    transaccion, sin que la capa de aplicacion dependa de Django.
    """

    @abstractmethod
    def __enter__(self) -> "UnidadDeTrabajo":
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, tipo_excepcion, excepcion, traceback) -> None:
        raise NotImplementedError


class RepositorioTutores(ABC):
    @abstractmethod
    def agregar(self, tutor: Tutor) -> Tutor:
        raise NotImplementedError

    @abstractmethod
    def obtener_por_id(self, tutor_id: int) -> Optional[Tutor]:
        raise NotImplementedError

    @abstractmethod
    def obtener_por_documento(self, documento: str) -> Optional[Tutor]:
        raise NotImplementedError

    @abstractmethod
    def listar(self) -> list[Tutor]:
        raise NotImplementedError


class RepositorioMascotas(ABC):
    @abstractmethod
    def agregar(self, mascota: Mascota) -> Mascota:
        raise NotImplementedError

    @abstractmethod
    def actualizar(self, mascota: Mascota) -> Mascota:
        raise NotImplementedError

    @abstractmethod
    def eliminar(self, mascota_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def obtener_por_id(self, mascota_id: int) -> Optional[Mascota]:
        raise NotImplementedError

    @abstractmethod
    def listar(self, tutor_id: Optional[int] = None) -> list[Mascota]:
        raise NotImplementedError


class RepositorioVeterinarios(ABC):
    @abstractmethod
    def agregar(self, veterinario: Veterinario) -> Veterinario:
        raise NotImplementedError

    @abstractmethod
    def obtener_por_id(self, veterinario_id: int) -> Optional[Veterinario]:
        raise NotImplementedError

    @abstractmethod
    def obtener_por_codigo(self, codigo: str) -> Optional[Veterinario]:
        raise NotImplementedError

    @abstractmethod
    def listar(self) -> list[Veterinario]:
        raise NotImplementedError


class FiltrosCitas:
    def __init__(
        self,
        fecha: Optional[date] = None,
        veterinario_id: Optional[int] = None,
        mascota_id: Optional[int] = None,
        estado: Optional[str] = None,
    ) -> None:
        self.fecha = fecha
        self.veterinario_id = veterinario_id
        self.mascota_id = mascota_id
        self.estado = estado


class RepositorioCitas(ABC):
    @abstractmethod
    def agregar(self, cita: Cita) -> Cita:
        raise NotImplementedError

    @abstractmethod
    def actualizar(self, cita: Cita) -> Cita:
        raise NotImplementedError

    @abstractmethod
    def obtener_por_id(self, cita_id: int) -> Optional[Cita]:
        raise NotImplementedError

    @abstractmethod
    def obtener_por_id_bloqueando(self, cita_id: int) -> Optional[Cita]:
        """Igual que obtener_por_id pero bajo SELECT FOR UPDATE dentro de una transaccion."""
        raise NotImplementedError

    @abstractmethod
    def existe_programada_veterinario_bloque(
        self, veterinario_id: int, fecha_hora: datetime
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def existe_programada_mascota_dia(self, mascota_id: int, fecha: date) -> bool:
        raise NotImplementedError

    @abstractmethod
    def contar_citas_del_dia(self, fecha: date) -> int:
        raise NotImplementedError

    @abstractmethod
    def obtener_agenda_dia(self, veterinario_id: int, fecha: date) -> list[Cita]:
        raise NotImplementedError

    @abstractmethod
    def listar(self, filtros: FiltrosCitas) -> list[Cita]:
        raise NotImplementedError


class Notificador(ABC):
    """Adapter target: formato de envio de un canal de notificacion."""

    @abstractmethod
    def enviar(self, destinatario: str, mensaje: str) -> str:
        """Envia el mensaje y devuelve el texto efectivamente emitido (para log/pruebas)."""
        raise NotImplementedError


class RepositorioNotificaciones(ABC):
    @abstractmethod
    def registrar(self, canal: str, destinatario: str, mensaje: str) -> None:
        raise NotImplementedError
