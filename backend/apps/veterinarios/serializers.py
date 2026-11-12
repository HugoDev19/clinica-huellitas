from rest_framework import serializers


class VeterinarioSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    codigo = serializers.CharField(max_length=20, trim_whitespace=True)
    nombre = serializers.CharField(max_length=150, trim_whitespace=True)
    disponible = serializers.BooleanField(read_only=True)
