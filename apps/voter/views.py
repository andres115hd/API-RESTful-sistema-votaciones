from rest_framework import generics

from apps.errors import save_or_validation_error

from .models import Voter
from .serializers import VoterSerializer


class VoterListCreateView(generics.ListCreateAPIView):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer

    def perform_create(self, serializer):
        save_or_validation_error(serializer)


class VoterDetailView(generics.RetrieveDestroyAPIView):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer
