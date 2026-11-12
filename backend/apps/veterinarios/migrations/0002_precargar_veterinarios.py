from django.db import migrations

VETERINARIOS_INICIALES = [
    {"codigo": "VET-01", "nombre": "Laura Gómez"},
    {"codigo": "VET-02", "nombre": "Andrés Ruiz"},
]


def precargar(apps, schema_editor):
    VeterinarioModel = apps.get_model("veterinarios", "VeterinarioModel")
    for datos in VETERINARIOS_INICIALES:
        VeterinarioModel.objects.get_or_create(
            codigo=datos["codigo"], defaults={"nombre": datos["nombre"], "disponible": True}
        )


def revertir(apps, schema_editor):
    VeterinarioModel = apps.get_model("veterinarios", "VeterinarioModel")
    codigos = [d["codigo"] for d in VETERINARIOS_INICIALES]
    VeterinarioModel.objects.filter(codigo__in=codigos).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("veterinarios", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(precargar, revertir),
    ]
