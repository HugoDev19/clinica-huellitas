class DomainError(Exception):
    """Excepcion base para violaciones de reglas de negocio del dominio."""

    codigo = "ERROR_DOMINIO"


class HorarioInvalidoError(DomainError):
    """RN1: fuera del horario de atencion o fuera de la grilla de 30 minutos."""

    codigo = "HORARIO_INVALIDO"


class VeterinarioNoDisponibleError(DomainError):
    """RN2: el veterinario ya tiene una cita PROGRAMADA en ese bloque."""

    codigo = "VETERINARIO_NO_DISPONIBLE"


class MascotaConCitaMismoDiaError(DomainError):
    """RN3: la mascota ya tiene una cita PROGRAMADA ese dia."""

    codigo = "MASCOTA_CON_CITA_MISMO_DIA"


class FechaFueraDeRangoError(DomainError):
    """RN4: la fecha no es futura o excede los 30 dias de anticipacion."""

    codigo = "FECHA_FUERA_DE_RANGO"


class CancelacionNoPermitidaError(DomainError):
    """RN5: faltan menos de dos horas para la cita o no esta PROGRAMADA."""

    codigo = "CANCELACION_NO_PERMITIDA"


class TransicionEstadoInvalidaError(DomainError):
    """RN8: la cita no esta en un estado desde el que se permita la transicion."""

    codigo = "TRANSICION_ESTADO_INVALIDA"


class EntidadNoEncontradaError(DomainError):
    codigo = "ENTIDAD_NO_ENCONTRADA"


class VeterinarioNoEncontradoError(EntidadNoEncontradaError):
    codigo = "VETERINARIO_NO_ENCONTRADO"


class MascotaNoEncontradaError(EntidadNoEncontradaError):
    codigo = "MASCOTA_NO_ENCONTRADA"


class MascotaConCitasError(DomainError):
    codigo = "MASCOTA_CON_CITAS"


class TutorNoEncontradoError(EntidadNoEncontradaError):
    codigo = "TUTOR_NO_ENCONTRADO"


class CitaNoEncontradaError(EntidadNoEncontradaError):
    codigo = "CITA_NO_ENCONTRADA"


class TutorDuplicadoError(DomainError):
    codigo = "TUTOR_DUPLICADO"


class VeterinarioDuplicadoError(DomainError):
    codigo = "VETERINARIO_DUPLICADO"
