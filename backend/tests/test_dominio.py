"""Pruebas unitarias del dominio puro: no requieren base de datos."""
from datetime import datetime
from decimal import Decimal

import pytest

from domain.entities import Cita, Mascota
from domain.enums import EstadoCita, TipoConsulta
from domain.exceptions import (
    CancelacionNoPermitidaError,
    FechaFueraDeRangoError,
    HorarioInvalidoError,
    TransicionEstadoInvalidaError,
)
from domain.reglas_horario import validar_horario_atencion, validar_rango_anticipacion
from domain.tarifas import TarifaEstandar, TarifaJornadaVacunacion
from domain.value_objects import CodigoCita


def _mascota(edad_anios: int) -> Mascota:
    return Mascota(id=1, nombre="Rex", especie="Perro", edad_anios=edad_anios, tutor_id=1)


def _cita(estado=EstadoCita.PROGRAMADA, fecha_hora=None) -> Cita:
    return Cita(
        id=1,
        codigo=CodigoCita("VET-20261117-001"),
        mascota_id=1,
        veterinario_id=1,
        fecha_hora=fecha_hora or datetime(2026, 11, 17, 10, 0),
        tipo_consulta=TipoConsulta.GENERAL,
        valor=Decimal("50000"),
        estado=estado,
    )


class TestReglasHorario:
    def test_rechaza_minutos_distintos_de_cero_o_treinta(self):
        with pytest.raises(HorarioInvalidoError):
            validar_horario_atencion(datetime(2026, 11, 17, 10, 15))

    def test_rechaza_hora_de_cierre_exacta(self):
        with pytest.raises(HorarioInvalidoError):
            validar_horario_atencion(datetime(2026, 11, 17, 17, 0))

    def test_rechaza_domingo(self):
        with pytest.raises(HorarioInvalidoError):
            validar_horario_atencion(datetime(2026, 11, 22, 10, 0))

    def test_acepta_sabado_dentro_de_horario(self):
        validar_horario_atencion(datetime(2026, 11, 21, 8, 0))  # no debe lanzar

    def test_rechaza_fecha_pasada(self):
        ahora = datetime(2026, 11, 17, 9, 0)
        with pytest.raises(FechaFueraDeRangoError):
            validar_rango_anticipacion(datetime(2026, 11, 17, 8, 0), ahora)

    def test_rechaza_mas_de_30_dias_de_anticipacion(self):
        ahora = datetime(2026, 11, 1, 8, 0)
        with pytest.raises(FechaFueraDeRangoError):
            validar_rango_anticipacion(datetime(2026, 12, 3, 8, 0), ahora)

    def test_acepta_dentro_de_30_dias(self):
        ahora = datetime(2026, 11, 1, 8, 0)
        validar_rango_anticipacion(datetime(2026, 11, 30, 8, 0), ahora)


class TestTarifaEstandar:
    def test_general_sin_descuento(self):
        valor = TarifaEstandar().calcular(TipoConsulta.GENERAL, _mascota(4), datetime(2026, 11, 17, 10, 0))
        assert valor == Decimal("50000")  # CA1

    def test_vacunacion_con_descuento_senior(self):
        valor = TarifaEstandar().calcular(
            TipoConsulta.VACUNACION, _mascota(12), datetime(2026, 11, 17, 9, 0)
        )
        assert valor == Decimal("31500")  # CA2

    def test_control_sin_descuento(self):
        valor = TarifaEstandar().calcular(TipoConsulta.CONTROL, _mascota(3), datetime(2026, 11, 17, 9, 0))
        assert valor == Decimal("25000")


class TestTarifaJornadaVacunacion:
    def test_sabado_vacunacion_veinte_por_ciento(self):
        sabado = datetime(2026, 11, 21, 10, 0)
        assert sabado.weekday() == 5
        valor = TarifaJornadaVacunacion().calcular(TipoConsulta.VACUNACION, _mascota(4), sabado)
        assert valor == Decimal("28000")

    def test_sabado_vacunacion_senior_no_acumula_descuentos(self):
        sabado = datetime(2026, 11, 21, 10, 0)
        valor = TarifaJornadaVacunacion().calcular(TipoConsulta.VACUNACION, _mascota(12), sabado)
        assert valor == Decimal("28000")  # max(20%, 10%), nunca 28% ni 30%

    def test_dia_entre_semana_delega_en_tarifa_estandar(self):
        martes = datetime(2026, 11, 17, 9, 0)
        valor = TarifaJornadaVacunacion().calcular(TipoConsulta.VACUNACION, _mascota(12), martes)
        assert valor == Decimal("31500")

    def test_general_no_afectado_aunque_sea_sabado(self):
        sabado = datetime(2026, 11, 21, 10, 0)
        valor = TarifaJornadaVacunacion().calcular(TipoConsulta.GENERAL, _mascota(4), sabado)
        assert valor == Decimal("50000")


class TestEstadosCita:
    def test_cancelar_programada_con_mas_de_dos_horas_de_anticipacion(self):
        cita = _cita(fecha_hora=datetime(2026, 11, 17, 10, 0))
        cita.cancelar(ahora=datetime(2026, 11, 17, 7, 0))
        assert cita.estado == EstadoCita.CANCELADA  # CA7

    def test_cancelar_con_menos_de_dos_horas_se_rechaza(self):
        cita = _cita(fecha_hora=datetime(2026, 11, 17, 10, 0))
        with pytest.raises(CancelacionNoPermitidaError):
            cita.cancelar(ahora=datetime(2026, 11, 17, 9, 0))  # CA8

    def test_atender_cita_cancelada_se_rechaza(self):
        cita = _cita(estado=EstadoCita.CANCELADA)
        with pytest.raises(TransicionEstadoInvalidaError):
            cita.atender()  # CA9

    def test_no_se_puede_cancelar_una_cita_ya_atendida(self):
        cita = _cita(estado=EstadoCita.ATENDIDA)
        with pytest.raises(TransicionEstadoInvalidaError):
            cita.cancelar(ahora=datetime(2026, 11, 17, 7, 0))

    def test_marcar_no_asistio_desde_programada(self):
        cita = _cita()
        cita.marcar_no_asistio()
        assert cita.estado == EstadoCita.NO_ASISTIO


class TestCodigoCita:
    def test_formato_generado(self):
        codigo = CodigoCita.generar(datetime(2026, 11, 17).date(), 3)
        assert str(codigo) == "VET-20261117-003"

    def test_secuencia_invalida(self):
        with pytest.raises(ValueError):
            CodigoCita.generar(datetime(2026, 11, 17).date(), 1000)
