from rest_framework import serializers

from tickets.models import Issue, Message, StatusChoice
from tickets.tasks import send_mail


CLOSE_ISSUE_TEXT = "Заявка закрыта."

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

    def update(self, instance, validated_data):
        if validated_data['status'] == StatusChoice.CLOSED:
            send_mail.delay(instance.pk, CLOSE_ISSUE_TEXT)
        return super().update(instance, validated_data)


class SendMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['body']

    def create(self, validated_data):
        issue = self.context.get('issue')
        if issue:
            if issue.status == StatusChoice.CLOSED:
                raise Exception("Issue already closed!")
            validated_data["issue_id"] = issue.pk
            validated_data["subject"] = issue.title
            send_mail.delay(issue.pk, validated_data.get('body'))
        return super().create(validated_data)
