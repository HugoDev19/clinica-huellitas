from rest_framework import serializers

from domain.enums import TipoConsulta


class CitaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    codigo = serializers.CharField(read_only=True)
    mascota_id = serializers.IntegerField()
    veterinario_id = serializers.IntegerField()
    fecha_hora = serializers.DateTimeField()
    tipo_consulta = serializers.ChoiceField(choices=[(t.value, t.value) for t in TipoConsulta])
    valor = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    estado = serializers.CharField(read_only=True)
    observaciones = serializers.CharField(required=False, allow_blank=True, default="")
    creado_en = serializers.DateTimeField(read_only=True)


class AtenderCitaSerializer(serializers.Serializer):
    observaciones = serializers.CharField(required=False, allow_blank=True, default="")


class DistribucionVeterinarioSerializer(serializers.Serializer):
    veterinario_id = serializers.IntegerField()
    total = serializers.IntegerField()


class DashboardSerializer(serializers.Serializer):
    fecha = serializers.DateField()
    total_citas = serializers.IntegerField()
    programadas = serializers.IntegerField()
    atendidas = serializers.IntegerField()
    canceladas = serializers.IntegerField()
    no_asistio = serializers.IntegerField()
    proximas_citas = CitaSerializer(many=True)
    distribucion_por_veterinario = DistribucionVeterinarioSerializer(many=True)
