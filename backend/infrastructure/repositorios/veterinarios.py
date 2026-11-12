from typing import Optional

from apps.veterinarios.models import VeterinarioModel
from domain.entities import Veterinario
from domain.ports import RepositorioVeterinarios


class RepositorioVeterinariosDjango(RepositorioVeterinarios):
    def obtener_por_id(self, veterinario_id: int) -> Optional[Veterinario]:
        modelo = VeterinarioModel.objects.filter(pk=veterinario_id).first()
        return self._a_entidad(modelo) if modelo else None

    def obtener_por_codigo(self, codigo: str) -> Optional[Veterinario]:
        modelo = VeterinarioModel.objects.filter(codigo=codigo).first()
        return self._a_entidad(modelo) if modelo else None

    def listar(self) -> list[Veterinario]:
        return [self._a_entidad(m) for m in VeterinarioModel.objects.all()]

    @staticmethod
    def _a_entidad(modelo: VeterinarioModel) -> Veterinario:
        return Veterinario(
            id=modelo.id, codigo=modelo.codigo, nombre=modelo.nombre, disponible=modelo.disponible
        )
