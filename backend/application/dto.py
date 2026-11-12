"""DTOs de entrada: contratos independientes de la representacion HTTP."""
from dataclasses import dataclass
from datetime import datetime

from domain.enums import TipoConsulta


@dataclass(frozen=True)
class RegistrarTutorDTO:
    nombre: str
    documento: str
    telefono: str
    correo: str


@dataclass(frozen=True)
class RegistrarMascotaDTO:
    nombre: str
    especie: str
    edad_anios: int
    tutor_id: int


@dataclass(frozen=True)
class AgendarCitaDTO:
    mascota_id: int
    veterinario_id: int
    fecha_hora: datetime
    tipo_consulta: TipoConsulta
    observaciones: str = ""


@dataclass(frozen=True)
class AtenderCitaDTO:
    cita_id: int
    observaciones: str = ""
