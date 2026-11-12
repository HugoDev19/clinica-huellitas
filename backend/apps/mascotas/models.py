from django.db import models


class MascotaModel(models.Model):
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)
    edad_anios = models.PositiveSmallIntegerField()
    tutor = models.ForeignKey(
        "tutores.TutorModel", on_delete=models.PROTECT, related_name="mascotas"
    )

    class Meta:
        db_table = "mascotas"
        ordering = ["nombre"]

    def __str__(self) -> str:
        return self.nombre
