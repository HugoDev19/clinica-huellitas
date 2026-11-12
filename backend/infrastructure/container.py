"""Composicion de dependencias (DI): une puertos del dominio con sus adaptadores.

La capa de presentacion solo conoce estas funciones fabrica; nunca instancia
repositorios ni adaptadores directamente.
"""
from django.conf import settings

from application.servicio_citas import ServicioCitas
from application.servicio_tutores_mascotas import ServicioTutoresMascotas
from application.servicio_veterinarios import ServicioVeterinarios
from domain.eventos import PublicadorEventosCita
from domain.observadores import ObservadorNotificacionTutor
from infrastructure.fabricas import fabricar_notificador, fabricar_politica_tarifa
from infrastructure.reloj import RelojSistema
from infrastructure.repositorios.citas import RepositorioCitasDjango
from infrastructure.repositorios.mascotas import RepositorioMascotasDjango
from infrastructure.repositorios.notificaciones import RepositorioNotificacionesDjango
from infrastructure.repositorios.tutores import RepositorioTutoresDjango
from infrastructure.repositorios.veterinarios import RepositorioVeterinariosDjango
from infrastructure.unidad_de_trabajo import UnidadDeTrabajoDjango


def construir_servicio_citas() -> ServicioCitas:
    publicador = PublicadorEventosCita()
    notificador = fabricar_notificador(settings.NOTIFICACION_CANAL)
    publicador.suscribir(
        ObservadorNotificacionTutor(notificador, RepositorioNotificacionesDjango())
    )

    return ServicioCitas(
        repo_citas=RepositorioCitasDjango(),
        repo_mascotas=RepositorioMascotasDjango(),
        repo_veterinarios=RepositorioVeterinariosDjango(),
        repo_tutores=RepositorioTutoresDjango(),
        reloj=RelojSistema(),
        politica_tarifa=fabricar_politica_tarifa(settings.POLITICA_TARIFA),
        publicador_eventos=publicador,
        uow=UnidadDeTrabajoDjango(),
    )


def construir_servicio_tutores_mascotas() -> ServicioTutoresMascotas:
    return ServicioTutoresMascotas(RepositorioTutoresDjango(), RepositorioMascotasDjango())


def construir_servicio_veterinarios() -> ServicioVeterinarios:
    return ServicioVeterinarios(RepositorioVeterinariosDjango())
