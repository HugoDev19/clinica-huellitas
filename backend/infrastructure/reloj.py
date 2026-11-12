from datetime import datetime

from django.utils import timezone

from domain.ports import Reloj


class RelojSistema(Reloj):
    """Implementacion real del reloj: usa la hora actual con zona horaria de Django."""

    def ahora(self) -> datetime:
        return timezone.now()
