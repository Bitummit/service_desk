from rest_framework import generics

from tickets.models import Issue
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .serilizers import IssueSerializer, IssueUpdateSerializer


class IssueListView(generics.ListAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['status']
    ordering_fields = ['created_at']


class IssueUpdateView(generics.UpdateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueUpdateSerializer