"""Dobles de prueba (test doubles) para los puertos del dominio."""
from datetime import datetime, timedelta
from typing import Optional

from domain.ports import Notificador, Reloj, RepositorioNotificaciones


class RelojFijo(Reloj):
    def __init__(self, ahora: datetime):
        self._ahora = ahora

    def ahora(self) -> datetime:
        return self._ahora

    def avanzar(self, **kwargs) -> None:
        self._ahora += timedelta(**kwargs)


class NotificadorEspia(Notificador):
    def __init__(self) -> None:
        self.mensajes_enviados: list[tuple[str, str]] = []

    def enviar(self, destinatario: str, mensaje: str) -> str:
        texto = f"[Espia a {destinatario}] {mensaje}"
        self.mensajes_enviados.append((destinatario, mensaje))
        return texto


class RepositorioNotificacionesEnMemoria(RepositorioNotificaciones):
    def __init__(self) -> None:
        self.registros: list[dict] = []

    def registrar(self, canal: str, destinatario: str, mensaje: str) -> None:
        self.registros.append({"canal": canal, "destinatario": destinatario, "mensaje": mensaje})
