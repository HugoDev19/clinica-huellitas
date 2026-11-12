import pytest

from application.dto import RegistrarMascotaDTO, RegistrarTutorDTO
from domain.exceptions import TutorDuplicadoError, TutorNoEncontradoError

pytestmark = pytest.mark.django_db


def test_cu1_registrar_tutor_y_mascota(servicio_tutores_mascotas):
    tutor = servicio_tutores_mascotas.registrar_tutor(
        RegistrarTutorDTO(nombre="Ana Ruiz", documento="CC-99", telefono="3001112222", correo="ana@example.com")
    )
    assert tutor.id is not None

    mascota = servicio_tutores_mascotas.registrar_mascota(
        RegistrarMascotaDTO(nombre="Firulais", especie="Perro", edad_anios=2, tutor_id=tutor.id)
    )
    assert mascota.tutor_id == tutor.id
    assert servicio_tutores_mascotas.listar_mascotas(tutor_id=tutor.id) == [mascota]


def test_rechaza_tutor_con_documento_duplicado(servicio_tutores_mascotas):
    dto = RegistrarTutorDTO(nombre="Ana Ruiz", documento="CC-99", telefono="3001112222", correo="ana@example.com")
    servicio_tutores_mascotas.registrar_tutor(dto)
    with pytest.raises(TutorDuplicadoError):
        servicio_tutores_mascotas.registrar_tutor(dto)


def test_rechaza_mascota_de_tutor_inexistente(servicio_tutores_mascotas):
    with pytest.raises(TutorNoEncontradoError):
        servicio_tutores_mascotas.registrar_mascota(
            RegistrarMascotaDTO(nombre="Firulais", especie="Perro", edad_anios=2, tutor_id=999)
        )


def test_veterinarios_precargados(servicio_veterinarios):
    codigos = {v.codigo for v in servicio_veterinarios.listar()}
    assert codigos == {"VET-01", "VET-02"}
