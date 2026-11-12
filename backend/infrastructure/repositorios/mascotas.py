from typing import Optional

from django.db.models.deletion import ProtectedError

from apps.mascotas.models import MascotaModel
from domain.entities import Mascota
from domain.exceptions import MascotaConCitasError
from domain.ports import RepositorioMascotas


class RepositorioMascotasDjango(RepositorioMascotas):
    def agregar(self, mascota: Mascota) -> Mascota:
        modelo = MascotaModel.objects.create(
            nombre=mascota.nombre,
            especie=mascota.especie,
            edad_anios=mascota.edad_anios,
            tutor_id=mascota.tutor_id,
        )
        return self._a_entidad(modelo)

    def actualizar(self, mascota: Mascota) -> Mascota:
        MascotaModel.objects.filter(pk=mascota.id).update(
            nombre=mascota.nombre,
            especie=mascota.especie,
            edad_anios=mascota.edad_anios,
            tutor_id=mascota.tutor_id,
        )
        modelo = MascotaModel.objects.get(pk=mascota.id)
        return self._a_entidad(modelo)

    def eliminar(self, mascota_id: int) -> None:
        try:
            MascotaModel.objects.filter(pk=mascota_id).delete()
        except ProtectedError as exc:
            raise MascotaConCitasError(
                "No se puede eliminar una mascota que tiene citas asociadas."
            ) from exc

    def obtener_por_id(self, mascota_id: int) -> Optional[Mascota]:
        modelo = MascotaModel.objects.filter(pk=mascota_id).first()
        return self._a_entidad(modelo) if modelo else None

    def listar(self, tutor_id: Optional[int] = None) -> list[Mascota]:
        qs = MascotaModel.objects.all()
        if tutor_id is not None:
            qs = qs.filter(tutor_id=tutor_id)
        return [self._a_entidad(m) for m in qs]

    @staticmethod
    def _a_entidad(modelo: MascotaModel) -> Mascota:
        return Mascota(
            id=modelo.id,
            nombre=modelo.nombre,
            especie=modelo.especie,
            edad_anios=modelo.edad_anios,
            tutor_id=modelo.tutor_id,
        )
