from django.db import models

from domain.enums import EstadoCita, TipoConsulta


class CitaModel(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    mascota = models.ForeignKey(
        "mascotas.MascotaModel", on_delete=models.PROTECT, related_name="citas"
    )
    veterinario = models.ForeignKey(
        "veterinarios.VeterinarioModel", on_delete=models.PROTECT, related_name="citas"
    )
    fecha_hora = models.DateTimeField()
    fecha = models.DateField(editable=False)
    tipo_consulta = models.CharField(
        max_length=20, choices=[(t.value, t.value) for t in TipoConsulta]
    )
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(
        max_length=20,
        choices=[(e.value, e.value) for e in EstadoCita],
        default=EstadoCita.PROGRAMADA.value,
    )
    observaciones = models.TextField(blank=True, default="")
    creado_en = models.DateTimeField()

    class Meta:
        db_table = "citas"
        ordering = ["fecha_hora"]
        indexes = [
            models.Index(fields=["veterinario", "fecha_hora"]),
            models.Index(fields=["mascota", "fecha"]),
            models.Index(fields=["fecha"]),
            models.Index(fields=["estado"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["veterinario", "fecha_hora"],
                condition=models.Q(estado="PROGRAMADA"),
                name="uq_veterinario_bloque_programada",
            ),
            models.UniqueConstraint(
                fields=["mascota", "fecha"],
                condition=models.Q(estado="PROGRAMADA"),
                name="uq_mascota_dia_programada",
            ),
        ]

    def save(self, *args, **kwargs):
        self.fecha = self.fecha_hora.date()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.codigo
