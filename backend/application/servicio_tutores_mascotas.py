"""Servicio de aplicacion para CU1: registrar tutor y mascota."""
from typing import Optional

from application.dto import RegistrarMascotaDTO, RegistrarTutorDTO
from domain.entities import Mascota, Tutor
from domain.exceptions import MascotaNoEncontradaError, TutorDuplicadoError, TutorNoEncontradoError
from domain.ports import RepositorioMascotas, RepositorioTutores


class ServicioTutoresMascotas:
    def __init__(self, repo_tutores: RepositorioTutores, repo_mascotas: RepositorioMascotas):
        self._repo_tutores = repo_tutores
        self._repo_mascotas = repo_mascotas

    def registrar_tutor(self, dto: RegistrarTutorDTO) -> Tutor:
        if self._repo_tutores.obtener_por_documento(dto.documento) is not None:
            raise TutorDuplicadoError(f"Ya existe un tutor con documento {dto.documento}")
        tutor = Tutor(
            nombre=dto.nombre, documento=dto.documento, telefono=dto.telefono, correo=dto.correo
        )
        return self._repo_tutores.agregar(tutor)

    def registrar_mascota(self, dto: RegistrarMascotaDTO) -> Mascota:
        if self._repo_tutores.obtener_por_id(dto.tutor_id) is None:
            raise TutorNoEncontradoError(f"No existe el tutor {dto.tutor_id}")
        mascota = Mascota(
            nombre=dto.nombre, especie=dto.especie, edad_anios=dto.edad_anios, tutor_id=dto.tutor_id
        )
        return self._repo_mascotas.agregar(mascota)

    def actualizar_mascota(self, mascota_id: int, dto: RegistrarMascotaDTO) -> Mascota:
        self.obtener_mascota(mascota_id)
        if self._repo_tutores.obtener_por_id(dto.tutor_id) is None:
            raise TutorNoEncontradoError(f"No existe el tutor {dto.tutor_id}")
        mascota = Mascota(
            id=mascota_id,
            nombre=dto.nombre,
            especie=dto.especie,
            edad_anios=dto.edad_anios,
            tutor_id=dto.tutor_id,
        )
        return self._repo_mascotas.actualizar(mascota)

    def eliminar_mascota(self, mascota_id: int) -> None:
        self.obtener_mascota(mascota_id)
        self._repo_mascotas.eliminar(mascota_id)

    def listar_tutores(self) -> list[Tutor]:
        return self._repo_tutores.listar()

    def obtener_tutor(self, tutor_id: int) -> Optional[Tutor]:
        return self._repo_tutores.obtener_por_id(tutor_id)

    def listar_mascotas(self, tutor_id: Optional[int] = None) -> list[Mascota]:
        return self._repo_mascotas.listar(tutor_id=tutor_id)

    def obtener_mascota(self, mascota_id: int) -> Mascota:
        mascota = self._repo_mascotas.obtener_por_id(mascota_id)
        if mascota is None:
            raise MascotaNoEncontradaError(f"No existe la mascota {mascota_id}")
        return mascota
