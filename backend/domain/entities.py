from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional

from domain.enums import EstadoCita, TipoConsulta
from domain.estados import obtener_estado
from domain.value_objects import CodigoCita

EDAD_MINIMA_DESCUENTO_SENIOR = 10


@dataclass
class Tutor:
    nombre: str
    documento: str
    telefono: str
    correo: str
    id: Optional[int] = None


@dataclass
class Mascota:
    nombre: str
    especie: str
    edad_anios: int
    tutor_id: int
    id: Optional[int] = None

    def es_senior(self) -> bool:
        return self.edad_anios >= EDAD_MINIMA_DESCUENTO_SENIOR


@dataclass
class Veterinario:
    codigo: str
    nombre: str
    disponible: bool = True
    id: Optional[int] = None


@dataclass
class Cita:
    codigo: CodigoCita
    mascota_id: int
    veterinario_id: int
    fecha_hora: datetime
    tipo_consulta: TipoConsulta
    valor: Decimal
    estado: EstadoCita = EstadoCita.PROGRAMADA
    observaciones: str = ""
    id: Optional[int] = None
    creado_en: Optional[datetime] = None

    def cancelar(self, ahora: datetime) -> None:
        obtener_estado(self.estado).cancelar(self, ahora)

    def atender(self, observaciones: str = "") -> None:
        obtener_estado(self.estado).atender(self, observaciones)

    def marcar_no_asistio(self) -> None:
        obtener_estado(self.estado).marcar_no_asistio(self)

    def esta_programada(self) -> bool:
        return self.estado == EstadoCita.PROGRAMADA
