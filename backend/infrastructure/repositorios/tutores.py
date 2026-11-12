from typing import Optional

from apps.tutores.models import TutorModel
from domain.entities import Tutor
from domain.ports import RepositorioTutores


class RepositorioTutoresDjango(RepositorioTutores):
    def agregar(self, tutor: Tutor) -> Tutor:
        modelo = TutorModel.objects.create(
            nombre=tutor.nombre,
            documento=tutor.documento,
            telefono=tutor.telefono,
            correo=tutor.correo,
        )
        return self._a_entidad(modelo)

    def obtener_por_id(self, tutor_id: int) -> Optional[Tutor]:
        modelo = TutorModel.objects.filter(pk=tutor_id).first()
        return self._a_entidad(modelo) if modelo else None

    def obtener_por_documento(self, documento: str) -> Optional[Tutor]:
        modelo = TutorModel.objects.filter(documento=documento).first()
        return self._a_entidad(modelo) if modelo else None

    def listar(self) -> list[Tutor]:
        return [self._a_entidad(m) for m in TutorModel.objects.all()]

    @staticmethod
    def _a_entidad(modelo: TutorModel) -> Tutor:
        return Tutor(
            id=modelo.id,
            nombre=modelo.nombre,
            documento=modelo.documento,
            telefono=modelo.telefono,
            correo=modelo.correo,
        )
