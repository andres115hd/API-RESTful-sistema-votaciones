from rest_framework import serializers

from .models import Candidate


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ["id", "name", "party", "votes"]
        read_only_fields = ["id", "votes"]
        extra_kwargs = {
            "name": {
                "error_messages": {
                    "required": "El nombre es obligatorio.",
                    "blank": "El nombre es obligatorio.",
                }
            },
            "party": {"required": False, "allow_null": True, "allow_blank": True},
        }
