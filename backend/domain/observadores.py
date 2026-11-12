"""Observador concreto: notifica al tutor cuando se agenda o cancela una cita (RN9).

Depende solo de los puertos Notificador y RepositorioNotificaciones, nunca de
un canal concreto. Que canal se use (consola, WhatsApp,...) se decide por
configuracion a traves de la fabrica correspondiente.
"""
from domain.eventos import CitaAgendada, CitaCancelada, EventoCita, ObservadorEventosCita
from domain.ports import Notificador, RepositorioNotificaciones


class ObservadorNotificacionTutor(ObservadorEventosCita):
    def __init__(self, notificador: Notificador, repositorio_notificaciones: RepositorioNotificaciones):
        self._notificador = notificador
        self._repositorio = repositorio_notificaciones

    def manejar(self, evento: EventoCita) -> None:
        mensaje = self._construir_mensaje(evento)
        texto_enviado = self._notificador.enviar(evento.tutor.telefono, mensaje)
        self._repositorio.registrar(
            canal=type(self._notificador).__name__,
            destinatario=evento.tutor.telefono,
            mensaje=texto_enviado,
        )

    @staticmethod
    def _construir_mensaje(evento: EventoCita) -> str:
        fecha_hora = evento.cita.fecha_hora.strftime("%d/%m/%Y %H:%M")
        if isinstance(evento, CitaAgendada):
            return (
                f"Hola {evento.tutor.nombre}, tu cita {evento.cita.codigo} para "
                f"{evento.mascota.nombre} ha sido agendada el {fecha_hora}."
            )
        if isinstance(evento, CitaCancelada):
            return (
                f"Hola {evento.tutor.nombre}, tu cita {evento.cita.codigo} para "
                f"{evento.mascota.nombre} del {fecha_hora} ha sido cancelada."
            )
        return f"Hola {evento.tutor.nombre}, tienes una actualizacion sobre tu cita {evento.cita.codigo}."
