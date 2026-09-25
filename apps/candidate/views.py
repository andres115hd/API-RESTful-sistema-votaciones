from rest_framework import generics

from apps.errors import save_or_validation_error

from .models import Candidate
from .serializers import CandidateSerializer


class CandidateListCreateView(generics.ListCreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

    def perform_create(self, serializer):
        save_or_validation_error(serializer)


class CandidateDetailView(generics.RetrieveDestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
