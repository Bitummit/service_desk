from lib2to3.fixes.fix_input import context

from rest_framework import generics

from tickets.models import Issue, Message
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import views
from .serilizers import IssueSerializer, IssueUpdateSerializer, SendMessageSerializer


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
    permission_classes = [IsAuthenticated]


class SendMessageAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SendMessageSerializer
    queryset = Message.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        issue_id = self.kwargs.get('issue_id')
        context['issue'] = Issue.objects.get(pk=issue_id)
        return context