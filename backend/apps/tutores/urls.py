from django.urls import path

from .views import TutorListCreateView

urlpatterns = [
    path("", TutorListCreateView.as_view(), name="tutores-list-create"),
]
