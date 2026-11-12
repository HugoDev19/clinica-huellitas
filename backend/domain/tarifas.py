"""Patron Strategy: politicas de calculo de tarifa (RN6 y escenario de cambio 1).

Permite agregar nuevas politicas de tarifa (por ejemplo jornadas especiales)
sin modificar el servicio de citas que las consume.
"""
from abc import ABC, abstractmethod
from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from typing import Optional

from domain.entities import Mascota
from domain.enums import TipoConsulta

SABADO = 5  # datetime.weekday(): lunes=0 ... domingo=6

TARIFAS_BASE: dict[TipoConsulta, Decimal] = {
    TipoConsulta.GENERAL: Decimal("50000"),
    TipoConsulta.VACUNACION: Decimal("35000"),
    TipoConsulta.CONTROL: Decimal("25000"),
}

DESCUENTO_SENIOR = Decimal("0.10")
DESCUENTO_JORNADA_VACUNACION = Decimal("0.20")


def _aplicar_descuento(base: Decimal, descuento: Decimal) -> Decimal:
    return (base * (Decimal("1") - descuento)).quantize(Decimal("1"), rounding=ROUND_HALF_UP)


class PoliticaTarifa(ABC):
    @abstractmethod
    def calcular(
        self, tipo_consulta: TipoConsulta, mascota: Mascota, fecha_hora: datetime
    ) -> Decimal:
        raise NotImplementedError


class TarifaEstandar(PoliticaTarifa):
    """RN6: tarifa base por tipo de consulta, con descuento del 10% para mascotas senior."""

    def calcular(
        self, tipo_consulta: TipoConsulta, mascota: Mascota, fecha_hora: datetime
    ) -> Decimal:
        base = TARIFAS_BASE[tipo_consulta]
        descuento = DESCUENTO_SENIOR if mascota.es_senior() else Decimal("0")
        return _aplicar_descuento(base, descuento)


class TarifaJornadaVacunacion(PoliticaTarifa):
    """Cambio 1: los sabados, VACUNACION tiene 20% de descuento.

    Si la mascota tambien es senior, se aplica unicamente el descuento mayor
    (no se acumulan). Para cualquier otro caso delega en la politica base.
    """

    def __init__(self, politica_base: Optional[PoliticaTarifa] = None):
        self._politica_base = politica_base or TarifaEstandar()

    def calcular(
        self, tipo_consulta: TipoConsulta, mascota: Mascota, fecha_hora: datetime
    ) -> Decimal:
        es_jornada_vacunacion = (
            tipo_consulta == TipoConsulta.VACUNACION and fecha_hora.weekday() == SABADO
        )
        if not es_jornada_vacunacion:
            return self._politica_base.calcular(tipo_consulta, mascota, fecha_hora)

        base = TARIFAS_BASE[tipo_consulta]
        descuento_senior = DESCUENTO_SENIOR if mascota.es_senior() else Decimal("0")
        descuento = max(DESCUENTO_JORNADA_VACUNACION, descuento_senior)
        return _aplicar_descuento(base, descuento)
