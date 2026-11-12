from django.urls import path

from .views import (
    AgendaDiariaView,
    AtenderCitaView,
    CancelarCitaView,
    CitaDetailView,
    CitaListCreateView,
    DashboardView,
    NoAsistioCitaView,
)

urlpatterns = [
    path("", CitaListCreateView.as_view(), name="citas-list-create"),
    path("agenda/", AgendaDiariaView.as_view(), name="citas-agenda"),
    path("dashboard/", DashboardView.as_view(), name="citas-dashboard"),
    path("<int:cita_id>/", CitaDetailView.as_view(), name="citas-detail"),
    path("<int:cita_id>/cancelar/", CancelarCitaView.as_view(), name="citas-cancelar"),
    path("<int:cita_id>/atender/", AtenderCitaView.as_view(), name="citas-atender"),
    path("<int:cita_id>/no-asistio/", NoAsistioCitaView.as_view(), name="citas-no-asistio"),
]
