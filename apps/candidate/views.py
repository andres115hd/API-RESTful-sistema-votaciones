from rest_framework import generics

from apps.errors import save_or_validation_error
from apps.pagination import StandardResultsSetPagination

from .models import Candidate
from .serializers import CandidateSerializer


class CandidateListCreateView(generics.ListCreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get("name")
        party = self.request.query_params.get("party")

        if name:
            queryset = queryset.filter(name__icontains=name.strip())
        if party:
            queryset = queryset.filter(party__icontains=party.strip())
        return queryset

    def perform_create(self, serializer):
        save_or_validation_error(serializer)


class CandidateDetailView(generics.RetrieveDestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
