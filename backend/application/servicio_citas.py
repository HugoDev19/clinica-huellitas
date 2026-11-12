"""Facade de aplicacion: coordina CU2-CU6 sin trasladar reglas de negocio a las vistas.

ServicioCitas es el unico punto de entrada que la capa de presentacion usa
para operar sobre citas. Las reglas de negocio (RN1-RN9) viven en el dominio;
este servicio orquesta repositorios, reloj, la politica de tarifa vigente y
la publicacion de eventos, sin conocer Django, DRF ni el canal de notificacion.
"""
from datetime import date

from application.dto import AgendarCitaDTO, AtenderCitaDTO
from domain.entities import Cita
from domain.enums import EstadoCita
from domain.eventos import CitaAgendada, CitaCancelada, PublicadorEventosCita
from domain.exceptions import (
    CitaNoEncontradaError,
    MascotaConCitaMismoDiaError,
    MascotaNoEncontradaError,
    TutorNoEncontradoError,
    VeterinarioNoDisponibleError,
    VeterinarioNoEncontradoError,
)
from domain.ports import (
    FiltrosCitas,
    Reloj,
    RepositorioCitas,
    RepositorioMascotas,
    RepositorioTutores,
    RepositorioVeterinarios,
    UnidadDeTrabajo,
)
from domain.reglas_horario import validar_horario_atencion, validar_rango_anticipacion
from domain.tarifas import PoliticaTarifa
from domain.value_objects import CodigoCita


class ServicioCitas:
    def __init__(
        self,
        repo_citas: RepositorioCitas,
        repo_mascotas: RepositorioMascotas,
        repo_veterinarios: RepositorioVeterinarios,
        repo_tutores: RepositorioTutores,
        reloj: Reloj,
        politica_tarifa: PoliticaTarifa,
        publicador_eventos: PublicadorEventosCita,
        uow: UnidadDeTrabajo,
    ) -> None:
        self._citas = repo_citas
        self._mascotas = repo_mascotas
        self._veterinarios = repo_veterinarios
        self._tutores = repo_tutores
        self._reloj = reloj
        self._politica_tarifa = politica_tarifa
        self._eventos = publicador_eventos
        self._uow = uow

    # CU2 -----------------------------------------------------------------
    def agendar_cita(self, dto: AgendarCitaDTO) -> Cita:
        mascota = self._mascotas.obtener_por_id(dto.mascota_id)
        if mascota is None:
            raise MascotaNoEncontradaError(f"No existe la mascota {dto.mascota_id}")

        veterinario = self._veterinarios.obtener_por_id(dto.veterinario_id)
        if veterinario is None:
            raise VeterinarioNoEncontradoError(f"No existe el veterinario {dto.veterinario_id}")

        tutor = self._tutores.obtener_por_id(mascota.tutor_id)
        if tutor is None:
            raise TutorNoEncontradoError(f"No existe el tutor {mascota.tutor_id}")

        ahora = self._reloj.ahora()
        validar_horario_atencion(dto.fecha_hora)
        validar_rango_anticipacion(dto.fecha_hora, ahora)

        with self._uow:
            if self._citas.existe_programada_veterinario_bloque(dto.veterinario_id, dto.fecha_hora):
                raise VeterinarioNoDisponibleError(
                    "El veterinario ya tiene una cita programada en ese horario"
                )

            if self._citas.existe_programada_mascota_dia(dto.mascota_id, dto.fecha_hora.date()):
                raise MascotaConCitaMismoDiaError(
                    "La mascota ya tiene una cita programada ese dia"
                )

            valor = self._politica_tarifa.calcular(dto.tipo_consulta, mascota, dto.fecha_hora)
            secuencia = self._citas.contar_citas_del_dia(dto.fecha_hora.date()) + 1
            codigo = CodigoCita.generar(dto.fecha_hora.date(), secuencia)

            cita = Cita(
                codigo=codigo,
                mascota_id=mascota.id,
                veterinario_id=veterinario.id,
                fecha_hora=dto.fecha_hora,
                tipo_consulta=dto.tipo_consulta,
                valor=valor,
                estado=EstadoCita.PROGRAMADA,
                observaciones=dto.observaciones,
                creado_en=ahora,
            )
            cita_guardada = self._citas.agregar(cita)
            self._eventos.publicar(CitaAgendada(cita=cita_guardada, mascota=mascota, tutor=tutor))
        return cita_guardada

    # CU3 -----------------------------------------------------------------
    def consultar_agenda_diaria(self, veterinario_id: int, fecha: date) -> list[Cita]:
        if self._veterinarios.obtener_por_id(veterinario_id) is None:
            raise VeterinarioNoEncontradoError(f"No existe el veterinario {veterinario_id}")
        return self._citas.obtener_agenda_dia(veterinario_id, fecha)

    # CU4 -----------------------------------------------------------------
    def cancelar_cita(self, cita_id: int) -> Cita:
        with self._uow:
            cita = self._citas.obtener_por_id_bloqueando(cita_id)
            if cita is None:
                raise CitaNoEncontradaError(f"No existe la cita {cita_id}")

            cita.cancelar(self._reloj.ahora())
            cita_actualizada = self._citas.actualizar(cita)

            mascota = self._mascotas.obtener_por_id(cita.mascota_id)
            tutor = self._tutores.obtener_por_id(mascota.tutor_id) if mascota else None
            if mascota and tutor:
                self._eventos.publicar(
                    CitaCancelada(cita=cita_actualizada, mascota=mascota, tutor=tutor)
                )
        return cita_actualizada

    # CU5 -----------------------------------------------------------------
    def atender_cita(self, dto: AtenderCitaDTO) -> Cita:
        with self._uow:
            cita = self._citas.obtener_por_id_bloqueando(dto.cita_id)
            if cita is None:
                raise CitaNoEncontradaError(f"No existe la cita {dto.cita_id}")
            cita.atender(dto.observaciones)
            cita_actualizada = self._citas.actualizar(cita)
        return cita_actualizada

    # CU6 -----------------------------------------------------------------
    def marcar_no_asistio(self, cita_id: int) -> Cita:
        with self._uow:
            cita = self._citas.obtener_por_id_bloqueando(cita_id)
            if cita is None:
                raise CitaNoEncontradaError(f"No existe la cita {cita_id}")
            cita.marcar_no_asistio()
            cita_actualizada = self._citas.actualizar(cita)
        return cita_actualizada

    def obtener_cita(self, cita_id: int) -> Cita:
        cita = self._citas.obtener_por_id(cita_id)
        if cita is None:
            raise CitaNoEncontradaError(f"No existe la cita {cita_id}")
        return cita

    def listar_citas(self, filtros: FiltrosCitas) -> list[Cita]:
        return self._citas.listar(filtros)
