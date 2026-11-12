from datetime import datetime

import pytest
from django.utils import timezone

from application.dto import RegistrarMascotaDTO, RegistrarTutorDTO
from application.servicio_citas import ServicioCitas
from application.servicio_tutores_mascotas import ServicioTutoresMascotas
from application.servicio_veterinarios import ServicioVeterinarios
from domain.eventos import PublicadorEventosCita
from domain.observadores import ObservadorNotificacionTutor
from infrastructure.fabricas import fabricar_politica_tarifa
from infrastructure.repositorios.citas import RepositorioCitasDjango
from infrastructure.repositorios.mascotas import RepositorioMascotasDjango
from infrastructure.repositorios.notificaciones import RepositorioNotificacionesDjango
from infrastructure.repositorios.tutores import RepositorioTutoresDjango
from infrastructure.repositorios.veterinarios import RepositorioVeterinariosDjango
from infrastructure.unidad_de_trabajo import UnidadDeTrabajoDjango

from .dobles import NotificadorEspia, RelojFijo


@pytest.fixture
def reloj_fijo():
    # Momento de referencia anterior a todas las fechas usadas en los criterios
    # de aceptacion (17/11/2026), para que las citas de prueba sean "futuras".
    return RelojFijo(timezone.make_aware(datetime(2026, 11, 1, 8, 0)))


@pytest.fixture
def notificador_espia():
    return NotificadorEspia()


@pytest.fixture
def servicio_tutores_mascotas(db):
    return ServicioTutoresMascotas(RepositorioTutoresDjango(), RepositorioMascotasDjango())


@pytest.fixture
def servicio_veterinarios(db):
    return ServicioVeterinarios(RepositorioVeterinariosDjango())


@pytest.fixture
def servicio_citas(db, reloj_fijo, notificador_espia):
    publicador = PublicadorEventosCita()
    publicador.suscribir(
        ObservadorNotificacionTutor(notificador_espia, RepositorioNotificacionesDjango())
    )
    return ServicioCitas(
        repo_citas=RepositorioCitasDjango(),
        repo_mascotas=RepositorioMascotasDjango(),
        repo_veterinarios=RepositorioVeterinariosDjango(),
        repo_tutores=RepositorioTutoresDjango(),
        reloj=reloj_fijo,
        politica_tarifa=fabricar_politica_tarifa("jornada_vacunacion"),
        publicador_eventos=publicador,
        uow=UnidadDeTrabajoDjango(),
    )


@pytest.fixture
def veterinario_laura(servicio_veterinarios):
    return _obtener(servicio_veterinarios, "VET-01")


@pytest.fixture
def veterinario_andres(servicio_veterinarios):
    return _obtener(servicio_veterinarios, "VET-02")


def _obtener(servicio_veterinarios, codigo):
    for veterinario in servicio_veterinarios.listar():
        if veterinario.codigo == codigo:
            return veterinario
    raise AssertionError(f"Veterinario {codigo} no esta precargado (revisar migracion de datos)")


@pytest.fixture
def tutor(servicio_tutores_mascotas):
    return servicio_tutores_mascotas.registrar_tutor(
        RegistrarTutorDTO(
            nombre="Carlos Perez", documento="CC-1", telefono="3000000001", correo="carlos@example.com"
        )
    )


@pytest.fixture
def max_mascota(servicio_tutores_mascotas, tutor):
    return servicio_tutores_mascotas.registrar_mascota(
        RegistrarMascotaDTO(nombre="Max", especie="Perro", edad_anios=4, tutor_id=tutor.id)
    )


@pytest.fixture
def luna_mascota_senior(servicio_tutores_mascotas, tutor):
    return servicio_tutores_mascotas.registrar_mascota(
        RegistrarMascotaDTO(nombre="Luna", especie="Gato", edad_anios=12, tutor_id=tutor.id)
    )
