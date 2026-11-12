from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from django.db import IntegrityError

from apps.citas.models import CitaModel
from domain.entities import Cita
from domain.enums import EstadoCita, TipoConsulta
from domain.exceptions import MascotaConCitaMismoDiaError, VeterinarioNoDisponibleError
from domain.ports import FiltrosCitas, RepositorioCitas
from domain.value_objects import CodigoCita


class RepositorioCitasDjango(RepositorioCitas):
    def agregar(self, cita: Cita) -> Cita:
        try:
            modelo = CitaModel.objects.create(
                codigo=str(cita.codigo),
                mascota_id=cita.mascota_id,
                veterinario_id=cita.veterinario_id,
                fecha_hora=cita.fecha_hora,
                tipo_consulta=cita.tipo_consulta.value,
                valor=cita.valor,
                estado=cita.estado.value,
                observaciones=cita.observaciones,
                creado_en=cita.creado_en,
            )
        except IntegrityError as exc:
            raise self._traducir_integridad(exc) from exc
        return self._a_entidad(modelo)

    def actualizar(self, cita: Cita) -> Cita:
        CitaModel.objects.filter(pk=cita.id).update(
            estado=cita.estado.value, observaciones=cita.observaciones
        )
        modelo = CitaModel.objects.get(pk=cita.id)
        return self._a_entidad(modelo)

    def obtener_por_id(self, cita_id: int) -> Optional[Cita]:
        modelo = CitaModel.objects.filter(pk=cita_id).first()
        return self._a_entidad(modelo) if modelo else None

    def obtener_por_id_bloqueando(self, cita_id: int) -> Optional[Cita]:
        modelo = CitaModel.objects.select_for_update().filter(pk=cita_id).first()
        return self._a_entidad(modelo) if modelo else None

    def existe_programada_veterinario_bloque(self, veterinario_id: int, fecha_hora: datetime) -> bool:
        return CitaModel.objects.filter(
            veterinario_id=veterinario_id,
            fecha_hora=fecha_hora,
            estado=EstadoCita.PROGRAMADA.value,
        ).exists()

    def existe_programada_mascota_dia(self, mascota_id: int, fecha: date) -> bool:
        return CitaModel.objects.filter(
            mascota_id=mascota_id, fecha=fecha, estado=EstadoCita.PROGRAMADA.value
        ).exists()

    def contar_citas_del_dia(self, fecha: date) -> int:
        return CitaModel.objects.filter(fecha=fecha).count()

    def obtener_agenda_dia(self, veterinario_id: int, fecha: date) -> list[Cita]:
        qs = CitaModel.objects.filter(veterinario_id=veterinario_id, fecha=fecha).order_by(
            "fecha_hora"
        )
        return [self._a_entidad(m) for m in qs]

    def listar(self, filtros: FiltrosCitas) -> list[Cita]:
        qs = CitaModel.objects.all()
        if filtros.fecha is not None:
            qs = qs.filter(fecha=filtros.fecha)
        if filtros.veterinario_id is not None:
            qs = qs.filter(veterinario_id=filtros.veterinario_id)
        if filtros.mascota_id is not None:
            qs = qs.filter(mascota_id=filtros.mascota_id)
        if filtros.estado is not None:
            qs = qs.filter(estado=filtros.estado)
        return [self._a_entidad(m) for m in qs.order_by("fecha_hora")]

    @staticmethod
    def _traducir_integridad(exc: IntegrityError) -> Exception:
        mensaje = str(exc).lower()
        if "uq_veterinario_bloque_programada" in mensaje:
            return VeterinarioNoDisponibleError(
                "El veterinario ya tiene una cita programada en ese horario"
            )
        if "uq_mascota_dia_programada" in mensaje:
            return MascotaConCitaMismoDiaError("La mascota ya tiene una cita programada ese dia")
        return exc

    @staticmethod
    def _a_entidad(modelo: CitaModel) -> Cita:
        return Cita(
            id=modelo.id,
            codigo=CodigoCita(modelo.codigo),
            mascota_id=modelo.mascota_id,
            veterinario_id=modelo.veterinario_id,
            fecha_hora=modelo.fecha_hora,
            tipo_consulta=TipoConsulta(modelo.tipo_consulta),
            valor=Decimal(modelo.valor),
            estado=EstadoCita(modelo.estado),
            observaciones=modelo.observaciones,
            creado_en=modelo.creado_en,
        )
