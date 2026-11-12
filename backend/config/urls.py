from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path(
        "",
        lambda request: JsonResponse(
            {
                "mensaje": "API de Clínica Veterinaria Huellitas",
                "estado": "funcionando",
                "documentacion": "/api/docs/",
                "veterinarios": "/api/veterinarios/",
                "tutores": "/api/tutores/",
                "mascotas": "/api/mascotas/",
                "citas": "/api/citas/",
            }
        ),
        name="api-root",
    ),
    path("admin/", admin.site.urls),
    path("api/tutores/", include("apps.tutores.urls")),
    path("api/mascotas/", include("apps.mascotas.urls")),
    path("api/veterinarios/", include("apps.veterinarios.urls")),
    path("api/citas/", include("apps.citas.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
