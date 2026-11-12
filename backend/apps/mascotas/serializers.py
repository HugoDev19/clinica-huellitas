from rest_framework import serializers


class MascotaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(max_length=100)
    especie = serializers.CharField(max_length=50)
    edad_anios = serializers.IntegerField(min_value=0, max_value=100)
    tutor_id = serializers.IntegerField()
