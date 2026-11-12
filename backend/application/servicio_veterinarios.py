from domain.entities import Veterinario
from domain.exceptions import VeterinarioNoEncontradoError
from domain.ports import RepositorioVeterinarios


class ServicioVeterinarios:
    def __init__(self, repo_veterinarios: RepositorioVeterinarios):
        self._repo = repo_veterinarios

    def listar(self) -> list[Veterinario]:
        return self._repo.listar()

    def obtener(self, veterinario_id: int) -> Veterinario:
        veterinario = self._repo.obtener_por_id(veterinario_id)
        if veterinario is None:
            raise VeterinarioNoEncontradoError(f"No existe el veterinario {veterinario_id}")
        return veterinario
