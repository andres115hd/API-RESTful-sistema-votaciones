from rest_framework import serializers

from .models import Voter


class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = ["id", "name", "email", "has_voted"]
        read_only_fields = ["id", "has_voted"]
        extra_kwargs = {
            "name": {
                "error_messages": {
                    "required": "El nombre es obligatorio.",
                    "blank": "El nombre es obligatorio.",
                }
            },
            "email": {
                "error_messages": {
                    "required": "El correo es obligatorio.",
                    "blank": "El correo es obligatorio.",
                    "invalid": "El correo no es válido.",
                    "unique": "Ya existe un votante con este correo.",
                }
            },
        }
