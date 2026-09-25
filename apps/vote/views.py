from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.errors import save_or_validation_error

from .models import Vote
from .serializers import VoteSerializer


class VoteListCreateView(generics.ListCreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def perform_create(self, serializer):
        save_or_validation_error(serializer)


class VoteStatisticsView(APIView):
    def get(self, request):
        return Response(Vote.get_statistics())
