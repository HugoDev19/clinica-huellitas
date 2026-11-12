from domain.entities import Veterinario
from domain.exceptions import VeterinarioDuplicadoError, VeterinarioNoEncontradoError
from domain.ports import RepositorioVeterinarios


class ServicioVeterinarios:
    def __init__(self, repo_veterinarios: RepositorioVeterinarios):
        self._repo = repo_veterinarios

    def listar(self) -> list[Veterinario]:
        return self._repo.listar()

    def registrar(self, codigo: str, nombre: str) -> Veterinario:
        codigo = codigo.strip().upper()
        nombre = nombre.strip()
        if self._repo.obtener_por_codigo(codigo) is not None:
            raise VeterinarioDuplicadoError(f"Ya existe un veterinario con código {codigo}")
        return self._repo.agregar(Veterinario(codigo=codigo, nombre=nombre))

    def obtener(self, veterinario_id: int) -> Veterinario:
        veterinario = self._repo.obtener_por_id(veterinario_id)
        if veterinario is None:
            raise VeterinarioNoEncontradoError(f"No existe el veterinario {veterinario_id}")
        return veterinario
