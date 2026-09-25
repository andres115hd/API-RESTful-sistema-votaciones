from rest_framework import serializers

from apps.candidate.models import Candidate
from apps.voter.models import Voter

from .models import Vote


class VoteSerializer(serializers.ModelSerializer):
    voter_id = serializers.PrimaryKeyRelatedField(
        source="voter",
        queryset=Voter.objects.all(),
        error_messages={
            "required": "El votante es obligatorio.",
            "does_not_exist": "El votante no existe.",
            "incorrect_type": "El votante no es válido.",
        },
    )
    candidate_id = serializers.PrimaryKeyRelatedField(
        source="candidate",
        queryset=Candidate.objects.all(),
        error_messages={
            "required": "El candidato es obligatorio.",
            "does_not_exist": "El candidato no es válido.",
            "incorrect_type": "El candidato no es válido.",
        },
    )

    class Meta:
        model = Vote
        fields = ["id", "voter_id", "candidate_id"]
        read_only_fields = ["id"]
