"""RN1 y RN4: validaciones puras sobre horario de atencion y rango de anticipacion."""
from datetime import datetime, timedelta

from domain.exceptions import FechaFueraDeRangoError, HorarioInvalidoError

HORA_APERTURA = 8
HORA_CIERRE = 17
DIAS_ATENCION = {0, 1, 2, 3, 4, 5}  # lunes(0) a sabado(5); domingo(6) excluido
MAX_DIAS_ANTICIPACION = 30


def validar_horario_atencion(fecha_hora: datetime) -> None:
    if fecha_hora.weekday() not in DIAS_ATENCION:
        raise HorarioInvalidoError("La clinica solo atiende de lunes a sabado")

    if fecha_hora.minute not in (0, 30) or fecha_hora.second != 0 or fecha_hora.microsecond != 0:
        raise HorarioInvalidoError("Las citas solo pueden iniciar cada 30 minutos en punto")

    hora_inicio = fecha_hora.replace(hour=HORA_APERTURA, minute=0, second=0, microsecond=0)
    hora_fin = fecha_hora.replace(hour=HORA_CIERRE, minute=0, second=0, microsecond=0)
    if not (hora_inicio <= fecha_hora < hora_fin):
        raise HorarioInvalidoError("El horario de atencion es de 8:00 a 17:00")


def validar_rango_anticipacion(fecha_hora: datetime, ahora: datetime) -> None:
    if fecha_hora <= ahora:
        raise FechaFueraDeRangoError("Solo se pueden agendar citas futuras")

    limite = ahora + timedelta(days=MAX_DIAS_ANTICIPACION)
    if fecha_hora > limite:
        raise FechaFueraDeRangoError(
            f"No se pueden agendar citas con mas de {MAX_DIAS_ANTICIPACION} dias de anticipacion"
        )
