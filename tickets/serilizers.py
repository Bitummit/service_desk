from rest_framework import serializers

from tickets.models import Issue, Message
from tickets.tasks import send_mail


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


class SendMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['body']

    def create(self, validated_data):
        issue = self.context.get('issue')
        if issue:
            validated_data["issue_id"] = issue.pk
            validated_data["subject"] = issue.title
        send_mail.delay(issue.pk, validated_data.get('body'))
        return super().create(validated_data)
