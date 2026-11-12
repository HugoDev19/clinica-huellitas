from rest_framework import serializers


class VeterinarioSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    codigo = serializers.CharField(max_length=20)
    nombre = serializers.CharField(max_length=150)
    disponible = serializers.BooleanField()
