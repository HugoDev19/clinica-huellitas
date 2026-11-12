from django.urls import path

from .views import VeterinarioDetailView, VeterinarioListView

urlpatterns = [
    path("", VeterinarioListView.as_view(), name="veterinarios-list"),
    path("<int:veterinario_id>/", VeterinarioDetailView.as_view(), name="veterinarios-detail"),
]
