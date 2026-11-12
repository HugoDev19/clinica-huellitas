from rest_framework import serializers


class TutorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(max_length=150)
    documento = serializers.CharField(max_length=30)
    telefono = serializers.CharField(max_length=30)
    correo = serializers.EmailField()
