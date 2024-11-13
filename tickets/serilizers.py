from rest_framework import serializers

from tickets.models import Issue, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['answer', 'subject', 'body']


class IssueSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Issue
        fields = ['title', 'status', 'client', 'created_at', 'manager', 'messages']


class IssueUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = ['status', 'manager']