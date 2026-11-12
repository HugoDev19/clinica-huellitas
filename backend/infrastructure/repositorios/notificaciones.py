from apps.notificaciones.models import NotificacionModel
from domain.ports import RepositorioNotificaciones


class RepositorioNotificacionesDjango(RepositorioNotificaciones):
    def registrar(self, canal: str, destinatario: str, mensaje: str) -> None:
        NotificacionModel.objects.create(canal=canal, destinatario=destinatario, mensaje=mensaje)
