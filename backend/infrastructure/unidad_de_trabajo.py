from django.db import transaction

from domain.ports import UnidadDeTrabajo


class UnidadDeTrabajoDjango(UnidadDeTrabajo):
    def __enter__(self) -> "UnidadDeTrabajoDjango":
        self._atomic = transaction.atomic()
        self._atomic.__enter__()
        return self

    def __exit__(self, tipo_excepcion, excepcion, traceback) -> None:
        return self._atomic.__exit__(tipo_excepcion, excepcion, traceback)
