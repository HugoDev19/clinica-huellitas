from enum import Enum


class TipoConsulta(str, Enum):
    GENERAL = "GENERAL"
    VACUNACION = "VACUNACION"
    CONTROL = "CONTROL"

    def __str__(self) -> str:  # evita "TipoConsulta.GENERAL" en serializacion/logs
        return self.value


class EstadoCita(str, Enum):
    PROGRAMADA = "PROGRAMADA"
    ATENDIDA = "ATENDIDA"
    CANCELADA = "CANCELADA"
    NO_ASISTIO = "NO_ASISTIO"

    def __str__(self) -> str:  # evita "EstadoCita.PROGRAMADA" en serializacion/logs
        return self.value
