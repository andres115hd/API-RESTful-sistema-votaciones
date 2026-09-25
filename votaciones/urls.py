"""
URL configuration for votaciones project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from apps.candidate.views import CandidateDetailView, CandidateListCreateView
from apps.vote.views import VoteListCreateView, VoteStatisticsView
from apps.voter.views import VoterDetailView, VoterListCreateView

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r"^voters/?$", VoterListCreateView.as_view(), name="voter-list"),
    re_path(r"^voters/(?P<pk>[0-9]+)/?$", VoterDetailView.as_view(), name="voter-detail"),
    re_path(r"^candidates/?$", CandidateListCreateView.as_view(), name="candidate-list"),
    re_path(
        r"^candidates/(?P<pk>[0-9]+)/?$",
        CandidateDetailView.as_view(),
        name="candidate-detail",
    ),
    re_path(r"^votes/statistics/?$", VoteStatisticsView.as_view(), name="vote-statistics"),
    re_path(r"^votes/?$", VoteListCreateView.as_view(), name="vote-list"),
]
