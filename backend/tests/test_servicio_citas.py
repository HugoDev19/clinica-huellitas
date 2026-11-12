"""Pruebas de integracion de CU2-CU6 contra la base de datos real (Postgres/sqlite)."""
from datetime import datetime
from decimal import Decimal

import pytest
from django.utils import timezone

from application.dto import AgendarCitaDTO, AtenderCitaDTO
from apps.notificaciones.models import NotificacionModel
from domain.enums import EstadoCita, TipoConsulta
from domain.exceptions import (
    CancelacionNoPermitidaError,
    FechaFueraDeRangoError,
    HorarioInvalidoError,
    MascotaConCitaMismoDiaError,
    TransicionEstadoInvalidaError,
    VeterinarioNoDisponibleError,
)
from domain.ports import FiltrosCitas

pytestmark = pytest.mark.django_db


def _aware(*args) -> datetime:
    return timezone.make_aware(datetime(*args))


def test_ca1_agendar_max_general(servicio_citas, max_mascota, veterinario_laura):
    cita = servicio_citas.agendar_cita(
        AgendarCitaDTO(
            mascota_id=max_mascota.id,
            veterinario_id=veterinario_laura.id,
            fecha_hora=_aware(2026, 11, 17, 10, 0),
            tipo_consulta=TipoConsulta.GENERAL,
        )
    )
    assert cita.valor == Decimal("50000")
    assert cita.estado == EstadoCita.PROGRAMADA
    assert cita.codigo.valor.startswith("VET-20261117-")


def test_ca2_agendar_luna_senior_vacunacion(servicio_citas, luna_mascota_senior, veterinario_andres):
    cita = servicio_citas.agendar_cita(
        AgendarCitaDTO(
            mascota_id=luna_mascota_senior.id,
            veterinario_id=veterinario_andres.id,
            fecha_hora=_aware(2026, 11, 17, 9, 0),
            tipo_consulta=TipoConsulta.VACUNACION,
        )
    )
    assert cita.valor == Decimal("31500")


@pytest.mark.parametrize(
    "fecha_hora",
    [
        datetime(2026, 11, 17, 10, 15),  # minutos invalidos
        datetime(2026, 11, 17, 17, 0),  # hora de cierre exacta
        datetime(2026, 11, 22, 10, 0),  # domingo
    ],
)
def test_ca3_rechaza_horarios_invalidos(servicio_citas, max_mascota, veterinario_laura, fecha_hora):
    with pytest.raises(HorarioInvalidoError):
        servicio_citas.agendar_cita(
            AgendarCitaDTO(
                mascota_id=max_mascota.id,
                veterinario_id=veterinario_laura.id,
                fecha_hora=timezone.make_aware(fecha_hora),
                tipo_consulta=TipoConsulta.GENERAL,
            )
        )


def test_ca4_rechaza_dos_citas_programadas_mismo_veterinario_mismo_bloque(
    servicio_citas, max_mascota, luna_mascota_senior, veterinario_laura
):
    fecha_hora = _aware(2026, 11, 17, 10, 0)
    servicio_citas.agendar_cita(
        AgendarCitaDTO(
            mascota_id=max_mascota.id,
            veterinario_id=veterinario_laura.id,
            fecha_hora=fecha_hora,
            tipo_consulta=TipoConsulta.GENERAL,
        )
    )
    with pytest.raises(VeterinarioNoDisponibleError):
        servicio_citas.agendar_cita(
            AgendarCitaDTO(
                mascota_id=luna_mascota_senior.id,
                veterinario_id=veterinario_laura.id,
                fecha_hora=fecha_hora,
                tipo_consulta=TipoConsulta.CONTROL,
            )
        )


def test_ca5_rechaza_dos_citas_programadas_misma_mascota_mismo_dia(
    servicio_citas, max_mascota, veterinario_laura, veterinario_andres
):
    servicio_citas.agendar_cita(
        AgendarCitaDTO(
            mascota_id=max_mascota.id,
            veterinario_id=veterinario_laura.id,
            fecha_hora=_aware(2026, 11, 17, 10, 0),
            tipo_consulta=TipoConsulta.GENERAL,
        )
    )
    with pytest.raises(MascotaConCitaMismoDiaError):
        servicio_citas.agendar_cita(
            AgendarCitaDTO(
                mascota_id=max_mascota.id,
                veterinario_id=veterinario_andres.id,
                fecha_hora=_aware(2026, 11, 17, 14, 0),
                tipo_consulta=TipoConsulta.CONTROL,
            )
        )


def test_ca6_rechaza_fecha_pasada_y_mas_de_30_dias(servicio_citas, max_mascota, veterinario_laura):
    # reloj_fijo esta en 2026-11-01 08:00
    with pytest.raises(FechaFueraDeRangoError):
        servicio_citas.agendar_cita(
            AgendarCitaDTO(
                mascota_id=max_mascota.id,
                veterinario_id=veterinario_laura.id,
                fecha_hora=_aware(2026, 10, 30, 10, 0),
                tipo_consulta=TipoConsulta.GENERAL,
            )
        )
    with pytest.raises(FechaFueraDeRangoError):
        servicio_citas.agendar_cita(
            AgendarCitaDTO(
                mascota_id=max_mascota.id,
                veterinario_id=veterinario_laura.id,
                fecha_hora=_aware(2026, 12, 3, 10, 0),
                tipo_consulta=TipoConsulta.GENERAL,
            )
        )


def test_ca7_cancelar_con_dos_horas_o_mas_libera_el_bloque(
    servicio_citas, max_mascota, luna_mascota_senior, veterinario_laura, reloj_fijo
):
    fecha_hora = _aware(2026, 11, 17, 10, 0)
    cita = servicio_citas.agendar_cita(
        AgendarCitaDTO(
            mascota_id=max_mascota.id,
            veterinario_id=veterinario_laura.id,
            fecha_hora=fecha_hora,
            tipo_consulta=TipoConsulta.GENERAL,
        )
    )
    reloj_fijo._ahora = _aware(2026, 11, 17, 7, 0)  # 3 horas antes
    cancelada = servicio_citas.cancelar_cita(cita.id)
    assert cancelada.estado == EstadoCita.CANCELADA

    # el bloque queda libre: otra mascota puede agendarse en el mismo horario
    nueva = servicio_citas.agendar_cita(
        AgendarCitaDTO(
            mascota_id=luna_mascota_senior.id,
            veterinario_id=veterinario_laura.id,
            fecha_hora=fecha_hora,
            tipo_consulta=TipoConsulta.CONTROL,
        )
    )
    assert nueva.estado == EstadoCita.PROGRAMADA


def test_ca8_rechaza_cancelacion_con_menos_de_dos_horas(
    servicio_citas, max_mascota, veterinario_laura, reloj_fijo
):
    fecha_hora = _aware(2026, 11, 17, 10, 0)
    cita = servicio_citas.agendar_cita(
        AgendarCitaDTO(
            mascota_id=max_mascota.id,
            veterinario_id=veterinario_laura.id,
            fecha_hora=fecha_hora,
            tipo_consulta=TipoConsulta.GENERAL,
        )
    )
    reloj_fijo._ahora = _aware(2026, 11, 17, 9, 0)  # 1 hora antes
    with pytest.raises(CancelacionNoPermitidaError):
        servicio_citas.cancelar_cita(cita.id)


def test_ca9_impide_atender_una_cita_cancelada(
    servicio_citas, max_mascota, veterinario_laura, reloj_fijo
):
    fecha_hora = _aware(2026, 11, 17, 10, 0)
    cita = servicio_citas.agendar_cita(
        AgendarCitaDTO(
            mascota_id=max_mascota.id,
            veterinario_id=veterinario_laura.id,
            fecha_hora=fecha_hora,
            tipo_consulta=TipoConsulta.GENERAL,
        )
    )
    servicio_citas.cancelar_cita(cita.id)
    with pytest.raises(TransicionEstadoInvalidaError):
        servicio_citas.atender_cita(AtenderCitaDTO(cita_id=cita.id, observaciones="Revision"))


def test_ca10_agenda_diaria_ordenada_cronologicamente(
    servicio_citas, max_mascota, luna_mascota_senior, veterinario_laura
):
    servicio_citas.agendar_cita(
        AgendarCitaDTO(
            mascota_id=max_mascota.id,
            veterinario_id=veterinario_laura.id,
            fecha_hora=_aware(2026, 11, 17, 14, 0),
            tipo_consulta=TipoConsulta.CONTROL,
        )
    )
    servicio_citas.agendar_cita(
        AgendarCitaDTO(
            mascota_id=luna_mascota_senior.id,
            veterinario_id=veterinario_laura.id,
            fecha_hora=_aware(2026, 11, 17, 9, 0),
            tipo_consulta=TipoConsulta.CONTROL,
        )
    )
    agenda = servicio_citas.consultar_agenda_diaria(veterinario_laura.id, _aware(2026, 11, 17, 0, 0).date())
    horas = [timezone.localtime(c.fecha_hora).hour for c in agenda]
    assert horas == sorted(horas)
    assert horas == [9, 14]


def test_marcar_no_asistio(servicio_citas, max_mascota, veterinario_laura):
    cita = servicio_citas.agendar_cita(
        AgendarCitaDTO(
            mascota_id=max_mascota.id,
            veterinario_id=veterinario_laura.id,
            fecha_hora=_aware(2026, 11, 17, 10, 0),
            tipo_consulta=TipoConsulta.GENERAL,
        )
    )
    actualizada = servicio_citas.marcar_no_asistio(cita.id)
    assert actualizada.estado == EstadoCita.NO_ASISTIO


def test_atender_cita_registra_observaciones(servicio_citas, max_mascota, veterinario_laura):
    cita = servicio_citas.agendar_cita(
        AgendarCitaDTO(
            mascota_id=max_mascota.id,
            veterinario_id=veterinario_laura.id,
            fecha_hora=_aware(2026, 11, 17, 10, 0),
            tipo_consulta=TipoConsulta.GENERAL,
        )
    )
    atendida = servicio_citas.atender_cita(
        AtenderCitaDTO(cita_id=cita.id, observaciones="Paciente estable")
    )
    assert atendida.estado == EstadoCita.ATENDIDA
    assert atendida.observaciones == "Paciente estable"


def test_filtrar_citas_por_estado_y_veterinario(servicio_citas, max_mascota, veterinario_laura):
    servicio_citas.agendar_cita(
        AgendarCitaDTO(
            mascota_id=max_mascota.id,
            veterinario_id=veterinario_laura.id,
            fecha_hora=_aware(2026, 11, 17, 10, 0),
            tipo_consulta=TipoConsulta.GENERAL,
        )
    )
    resultado = servicio_citas.listar_citas(
        FiltrosCitas(veterinario_id=veterinario_laura.id, estado=EstadoCita.PROGRAMADA.value)
    )
    assert len(resultado) == 1


class TestNotificacionesYEventos:
    def test_agendar_notifica_al_tutor_por_whatsapp(
        self, servicio_citas, max_mascota, veterinario_laura, notificador_espia
    ):
        servicio_citas.agendar_cita(
            AgendarCitaDTO(
                mascota_id=max_mascota.id,
                veterinario_id=veterinario_laura.id,
                fecha_hora=_aware(2026, 11, 17, 10, 0),
                tipo_consulta=TipoConsulta.GENERAL,
            )
        )
        assert len(notificador_espia.mensajes_enviados) == 1
        destinatario, mensaje = notificador_espia.mensajes_enviados[0]
        assert destinatario == "3000000001"
        assert "agendada" in mensaje
        assert NotificacionModel.objects.count() == 1

    def test_cancelar_notifica_al_tutor(
        self, servicio_citas, max_mascota, veterinario_laura, notificador_espia, reloj_fijo
    ):
        cita = servicio_citas.agendar_cita(
            AgendarCitaDTO(
                mascota_id=max_mascota.id,
                veterinario_id=veterinario_laura.id,
                fecha_hora=_aware(2026, 11, 17, 10, 0),
                tipo_consulta=TipoConsulta.GENERAL,
            )
        )
        notificador_espia.mensajes_enviados.clear()
        reloj_fijo._ahora = _aware(2026, 11, 17, 7, 0)
        servicio_citas.cancelar_cita(cita.id)
        assert len(notificador_espia.mensajes_enviados) == 1
        assert "cancelada" in notificador_espia.mensajes_enviados[0][1]

    def test_formato_adaptador_whatsapp_real(self):
        from infrastructure.notificadores import NotificadorWhatsApp

        texto = NotificadorWhatsApp().enviar("3000000001", "Hola")
        assert texto == "[WhatsApp a 3000000001] Hola"

    def test_formato_adaptador_consola(self):
        from infrastructure.notificadores import NotificadorConsola

        texto = NotificadorConsola().enviar("3000000001", "Hola")
        assert texto == "[Consola a 3000000001] Hola"
