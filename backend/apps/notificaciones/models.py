from django.db import models


class NotificacionModel(models.Model):
    canal = models.CharField(max_length=50)
    destinatario = models.CharField(max_length=100)
    mensaje = models.TextField()
    enviado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notificaciones"
        ordering = ["-enviado_en"]

    def __str__(self) -> str:
        return f"[{self.canal}] {self.destinatario}"
