from rest_framework import generics

from apps.errors import save_or_validation_error
from apps.pagination import StandardResultsSetPagination

from .models import Voter
from .serializers import VoterSerializer


class VoterListCreateView(generics.ListCreateAPIView):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get("name")
        email = self.request.query_params.get("email")
        has_voted = self.request.query_params.get("has_voted")

        if name:
            queryset = queryset.filter(name__icontains=name.strip())
        if email:
            queryset = queryset.filter(email__icontains=email.strip())
        if has_voted not in (None, ""):
            normalized = has_voted.strip().lower()
            if normalized in ("true", "1"):
                queryset = queryset.filter(has_voted=True)
            elif normalized in ("false", "0"):
                queryset = queryset.filter(has_voted=False)
        return queryset

    def perform_create(self, serializer):
        save_or_validation_error(serializer)


class VoterDetailView(generics.RetrieveDestroyAPIView):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer
