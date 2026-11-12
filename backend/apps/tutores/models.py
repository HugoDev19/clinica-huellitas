from django.db import models


class TutorModel(models.Model):
    nombre = models.CharField(max_length=150)
    documento = models.CharField(max_length=30, unique=True)
    telefono = models.CharField(max_length=30)
    correo = models.EmailField()

    class Meta:
        db_table = "tutores"
        ordering = ["nombre"]

    def __str__(self) -> str:
        return f"{self.nombre} ({self.documento})"
