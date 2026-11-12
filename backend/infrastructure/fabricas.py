"""Factory Method: elige la implementacion concreta segun configuracion.

Asi se incorporan NotificadorWhatsApp y TarifaJornadaVacunacion (escenario de
cambio) sin modificar ServicioCitas: basta registrar la clase aqui y ajustar
una variable de entorno.
"""
from domain.ports import Notificador
from domain.tarifas import PoliticaTarifa, TarifaEstandar, TarifaJornadaVacunacion
from infrastructure.notificadores import NotificadorConsola, NotificadorWhatsApp

_NOTIFICADORES: dict[str, type[Notificador]] = {
    "consola": NotificadorConsola,
    "whatsapp": NotificadorWhatsApp,
}

_POLITICAS_TARIFA: dict[str, type[PoliticaTarifa]] = {
    "estandar": TarifaEstandar,
    "jornada_vacunacion": TarifaJornadaVacunacion,
}


def fabricar_notificador(canal: str) -> Notificador:
    clase = _NOTIFICADORES.get(canal.lower())
    if clase is None:
        disponibles = ", ".join(_NOTIFICADORES)
        raise ValueError(f"Canal de notificacion '{canal}' no soportado. Opciones: {disponibles}")
    return clase()


def fabricar_politica_tarifa(nombre: str) -> PoliticaTarifa:
    clase = _POLITICAS_TARIFA.get(nombre.lower())
    if clase is None:
        disponibles = ", ".join(_POLITICAS_TARIFA)
        raise ValueError(f"Politica de tarifa '{nombre}' no soportada. Opciones: {disponibles}")
    return clase()
