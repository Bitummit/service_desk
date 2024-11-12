from django.db import models
from django.contrib.auth.models import User


class StatusChoice(models.TextChoices):
    CREATED = 'created', 'Created'
    IN_PROGRESS = 'in_progress', 'In progress'
    CLOSED = 'closed', 'Closed'


class Issue(models.Model):
    title = models.CharField(max_length=256, verbose_name="Тема")
    status = models.CharField(max_length=16, choices=StatusChoice, default=StatusChoice.CREATED, verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="Дата обращения")
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="Дата обновления")
    manager = models.ForeignKey(User, related_name="issues", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Исполнитель")
    client = models.EmailField(max_length=256, verbose_name="От кого")

    def __str__(self):
        return f"[Issue #{self.pk}]"

class Message(models.Model):
    subject = models.CharField(max_length=256, verbose_name="Тема")
    body = models.TextField(verbose_name="Содержание")
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="messages",verbose_name="Обращение")

    def __str__(self):
        return f"{self.subject}"