"""Pruebas de aceptacion a nivel de API REST (capa de presentacion completa)."""
from datetime import datetime

import pytest
from django.utils import timezone
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture(autouse=True)
def reloj_api_fijo(monkeypatch):
    momento = timezone.make_aware(datetime(2026, 11, 1, 8, 0))
    monkeypatch.setattr("infrastructure.reloj.RelojSistema.ahora", lambda self: momento)


@pytest.fixture
def tutor_id(client):
    respuesta = client.post(
        "/api/tutores/",
        {"nombre": "Carlos Perez", "documento": "CC-API-1", "telefono": "3000000001", "correo": "carlos@example.com"},
        format="json",
    )
    assert respuesta.status_code == 201, respuesta.data
    return respuesta.data["id"]


@pytest.fixture
def mascota_id(client, tutor_id):
    respuesta = client.post(
        "/api/mascotas/",
        {"nombre": "Max", "especie": "Perro", "edad_anios": 4, "tutor_id": tutor_id},
        format="json",
    )
    assert respuesta.status_code == 201, respuesta.data
    return respuesta.data["id"]


@pytest.fixture
def veterinario_id(client):
    respuesta = client.get("/api/veterinarios/")
    assert respuesta.status_code == 200
    return respuesta.data[0]["id"]


def test_flujo_completo_agendar_consultar_y_cancelar(client, mascota_id, veterinario_id):
    respuesta = client.post(
        "/api/citas/",
        {
            "mascota_id": mascota_id,
            "veterinario_id": veterinario_id,
            "fecha_hora": "2026-11-17T10:00:00-05:00",
            "tipo_consulta": "GENERAL",
        },
        format="json",
    )
    assert respuesta.status_code == 201, respuesta.data
    cita_id = respuesta.data["id"]
    assert respuesta.data["estado"] == "PROGRAMADA"
    assert respuesta.data["tipo_consulta"] == "GENERAL"
    assert respuesta.data["valor"] == "50000.00"

    detalle = client.get(f"/api/citas/{cita_id}/")
    assert detalle.status_code == 200
    assert detalle.data["codigo"].startswith("VET-20261117-")

    agenda = client.get(f"/api/citas/agenda/?veterinario_id={veterinario_id}&fecha=2026-11-17")
    assert agenda.status_code == 200
    assert len(agenda.data) == 1

    cancelacion = client.post(f"/api/citas/{cita_id}/cancelar/")
    assert cancelacion.status_code == 200, cancelacion.data
    assert cancelacion.data["estado"] == "CANCELADA"


def test_flujo_atender_y_marcar_no_asistio(client, mascota_id, tutor_id, veterinario_id):
    segunda_mascota = client.post(
        "/api/mascotas/",
        {"nombre": "Luna", "especie": "Gata", "edad_anios": 3, "tutor_id": tutor_id},
        format="json",
    )
    assert segunda_mascota.status_code == 201, segunda_mascota.data

    cita_atendida = client.post(
        "/api/citas/",
        {
            "mascota_id": mascota_id,
            "veterinario_id": veterinario_id,
            "fecha_hora": "2026-11-17T10:00:00-05:00",
            "tipo_consulta": "GENERAL",
        },
        format="json",
    )
    cita_no_asistio = client.post(
        "/api/citas/",
        {
            "mascota_id": segunda_mascota.data["id"],
            "veterinario_id": veterinario_id,
            "fecha_hora": "2026-11-17T11:00:00-05:00",
            "tipo_consulta": "CONTROL",
        },
        format="json",
    )
    assert cita_atendida.status_code == 201, cita_atendida.data
    assert cita_no_asistio.status_code == 201, cita_no_asistio.data

    atendida = client.post(
        f"/api/citas/{cita_atendida.data['id']}/atender/",
        {"observaciones": "Paciente estable"},
        format="json",
    )
    no_asistio = client.post(f"/api/citas/{cita_no_asistio.data['id']}/no-asistio/")

    assert atendida.status_code == 200, atendida.data
    assert atendida.data["estado"] == "ATENDIDA"
    assert atendida.data["observaciones"] == "Paciente estable"
    assert no_asistio.status_code == 200, no_asistio.data
    assert no_asistio.data["estado"] == "NO_ASISTIO"


def test_flujo_completo_cu1_a_cu6_por_api(client, veterinario_id):
    tutor = client.post(
        "/api/tutores/",
        {
            "nombre": "María López",
            "documento": "CC-CU1-CU6",
            "telefono": "3001234567",
            "correo": "maria@example.com",
        },
        format="json",
    )
    assert tutor.status_code == 201, tutor.data

    mascotas = []
    for nombre in ("Nube", "Milo", "Luna"):
        respuesta = client.post(
            "/api/mascotas/",
            {
                "nombre": nombre,
                "especie": "Gato",
                "edad_anios": 3,
                "tutor_id": tutor.data["id"],
            },
            format="json",
        )
        assert respuesta.status_code == 201, respuesta.data
        mascotas.append(respuesta.data)

    citas = []
    for mascota, hora, tipo in zip(
        mascotas, ("09:00", "10:00", "11:00"), ("GENERAL", "CONTROL", "VACUNACION")
    ):
        respuesta = client.post(
            "/api/citas/",
            {
                "mascota_id": mascota["id"],
                "veterinario_id": veterinario_id,
                "fecha_hora": f"2026-11-17T{hora}:00-05:00",
                "tipo_consulta": tipo,
            },
            format="json",
        )
        assert respuesta.status_code == 201, respuesta.data
        citas.append(respuesta.data)

    agenda = client.get(
        f"/api/citas/agenda/?veterinario_id={veterinario_id}&fecha=2026-11-17"
    )
    assert agenda.status_code == 200, agenda.data
    assert [cita["id"] for cita in agenda.data] == [cita["id"] for cita in citas]

    cancelada = client.post(f"/api/citas/{citas[0]['id']}/cancelar/")
    atendida = client.post(
        f"/api/citas/{citas[1]['id']}/atender/",
        {"observaciones": "Revisión general; paciente estable."},
        format="json",
    )
    no_asistio = client.post(f"/api/citas/{citas[2]['id']}/no-asistio/")

    assert cancelada.status_code == 200, cancelada.data
    assert cancelada.data["estado"] == "CANCELADA"
    assert atendida.status_code == 200, atendida.data
    assert atendida.data["estado"] == "ATENDIDA"
    assert atendida.data["observaciones"] == "Revisión general; paciente estable."
    assert no_asistio.status_code == 200, no_asistio.data
    assert no_asistio.data["estado"] == "NO_ASISTIO"


def test_rechaza_patch_arbitrario_de_estado(client, mascota_id, veterinario_id):
    respuesta = client.post(
        "/api/citas/",
        {
            "mascota_id": mascota_id,
            "veterinario_id": veterinario_id,
            "fecha_hora": "2026-11-17T11:00:00-05:00",
            "tipo_consulta": "CONTROL",
        },
        format="json",
    )
    cita_id = respuesta.data["id"]
    patch = client.patch(f"/api/citas/{cita_id}/", {"estado": "ATENDIDA"}, format="json")
    assert patch.status_code == 405  # no existe PATCH: solo endpoints de accion explicitos


def test_dashboard_endpoint_responde(client, mascota_id, veterinario_id):
    client.post(
        "/api/citas/",
        {
            "mascota_id": mascota_id,
            "veterinario_id": veterinario_id,
            "fecha_hora": "2026-11-17T10:00:00-05:00",
            "tipo_consulta": "GENERAL",
        },
        format="json",
    )
    respuesta = client.get("/api/citas/dashboard/?fecha=2026-11-17")
    assert respuesta.status_code == 200
    assert respuesta.data["total_citas"] == 1
    assert respuesta.data["programadas"] == 1


def test_documento_duplicado_devuelve_409(client):
    datos = {"nombre": "Carlos", "documento": "CC-DUP", "telefono": "300", "correo": "c@example.com"}
    assert client.post("/api/tutores/", datos, format="json").status_code == 201
    respuesta = client.post("/api/tutores/", datos, format="json")
    assert respuesta.status_code == 409
    assert respuesta.data["error"] == "TUTOR_DUPLICADO"


def test_crear_veterinario(client):
    respuesta = client.post(
        "/api/veterinarios/",
        {"codigo": "vet-test-01", "nombre": "Diana Gómez"},
        format="json",
    )
    assert respuesta.status_code == 201, respuesta.data
    assert respuesta.data["codigo"] == "VET-TEST-01"
    assert respuesta.data["nombre"] == "Diana Gómez"
    assert respuesta.data["disponible"] is True


def test_codigo_veterinario_duplicado_devuelve_409(client):
    datos = {"codigo": "VET-DUP-API", "nombre": "Diana Gómez"}
    assert client.post("/api/veterinarios/", datos, format="json").status_code == 201
    respuesta = client.post(
        "/api/veterinarios/",
        {"codigo": "vet-dup-api", "nombre": "Otro nombre"},
        format="json",
    )
    assert respuesta.status_code == 409
    assert respuesta.data["error"] == "VETERINARIO_DUPLICADO"


def test_mascota_inexistente_devuelve_404(client):
    respuesta = client.get("/api/mascotas/999999/")
    assert respuesta.status_code == 404
    assert respuesta.data["error"] == "MASCOTA_NO_ENCONTRADA"


def test_actualizar_mascota(client, mascota_id, tutor_id):
    respuesta = client.put(
        f"/api/mascotas/{mascota_id}/",
        {"nombre": "Luna", "especie": "Gata", "edad_anios": 3, "tutor_id": tutor_id},
        format="json",
    )
    assert respuesta.status_code == 200
    assert respuesta.data["nombre"] == "Luna"
    assert respuesta.data["especie"] == "Gata"
    assert client.get(f"/api/mascotas/{mascota_id}/").data["nombre"] == "Luna"


def test_eliminar_mascota_sin_citas(client, mascota_id):
    respuesta = client.delete(f"/api/mascotas/{mascota_id}/")
    assert respuesta.status_code == 204
    assert client.get(f"/api/mascotas/{mascota_id}/").status_code == 404


def test_no_eliminar_mascota_con_citas(client, mascota_id, veterinario_id):
    cita = client.post(
        "/api/citas/",
        {
            "mascota_id": mascota_id,
            "veterinario_id": veterinario_id,
            "fecha_hora": "2026-11-17T10:00:00-05:00",
            "tipo_consulta": "GENERAL",
        },
        format="json",
    )
    assert cita.status_code == 201, cita.data

    respuesta = client.delete(f"/api/mascotas/{mascota_id}/")
    assert respuesta.status_code == 409
    assert respuesta.data["error"] == "MASCOTA_CON_CITAS"
