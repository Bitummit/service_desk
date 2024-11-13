from django.db.models import Q
from rest_framework import generics
from tickets.models import Issue, Message, StatusChoice
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .serilizers import IssueSerializer, IssueUpdateSerializer, SendMessageSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status


class IssueListView(generics.ListAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['status']
    ordering_fields = ['created_at']


class IssueUpdateView(generics.UpdateAPIView):
    queryset = Issue.objects.filter(~Q(status=StatusChoice.CLOSED))
    serializer_class = IssueUpdateSerializer
    permission_classes = [IsAuthenticated]


class SendMessageAPIView(generics.CreateAPIView):
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = SendMessageSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        issue_id = self.kwargs.get('pk')
        issue = Issue.objects.get(pk=issue_id)
        context['issue'] = issue
        return context

    @swagger_auto_schema(request_body=SendMessageSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)