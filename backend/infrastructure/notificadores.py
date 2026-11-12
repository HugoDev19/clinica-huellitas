"""Patron Adapter: cada canal de notificacion adapta el mismo puerto Notificador.

Agregar un canal nuevo (correo, SMS, un proveedor externo...) consiste en
anadir una clase aqui e inscribirla en infrastructure.fabricas, sin tocar el
dominio ni la aplicacion.
"""
import logging

from domain.ports import Notificador

logger = logging.getLogger("notificaciones")


class NotificadorConsola(Notificador):
    def enviar(self, destinatario: str, mensaje: str) -> str:
        texto = f"[Consola a {destinatario}] {mensaje}"
        logger.info(texto)
        return texto


class NotificadorWhatsApp(Notificador):
    """Simulacion funcional de envio de WhatsApp (sin proveedor externo real)."""

    def enviar(self, destinatario: str, mensaje: str) -> str:
        texto = f"[WhatsApp a {destinatario}] {mensaje}"
        logger.info(texto)
        return texto
