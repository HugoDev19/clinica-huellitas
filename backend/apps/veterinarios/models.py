from django.db import models


class VeterinarioModel(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=150)
    disponible = models.BooleanField(default=True)

    class Meta:
        db_table = "veterinarios"
        ordering = ["codigo"]

    def __str__(self) -> str:
        return f"{self.codigo} - {self.nombre}"
