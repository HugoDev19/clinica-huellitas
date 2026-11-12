from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class CodigoCita:
    """Codigo unico de cita con formato VET-AAAAMMDD-NNN (RN7)."""

    valor: str

    @staticmethod
    def generar(fecha: date, secuencia: int) -> "CodigoCita":
        if secuencia < 1 or secuencia > 999:
            raise ValueError("La secuencia del codigo de cita debe estar entre 1 y 999")
        return CodigoCita(f"VET-{fecha.strftime('%Y%m%d')}-{secuencia:03d}")

    def __str__(self) -> str:
        return self.valor
