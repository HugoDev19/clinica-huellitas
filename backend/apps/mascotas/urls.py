from django.urls import path

from .views import MascotaDetailView, MascotaListCreateView

urlpatterns = [
    path("", MascotaListCreateView.as_view(), name="mascotas-list-create"),
    path("<int:mascota_id>/", MascotaDetailView.as_view(), name="mascotas-detail"),
]
