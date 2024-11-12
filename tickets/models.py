from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Issue(models.Model):
    title = models.CharField(max_length=256, verbose_name="Тема")
    date = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="Дата обращения")
    manager = models.ForeignKey(User, related_name="issues", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Исполнитель")
    client = models.EmailField(max_length=256, verbose_name="От кого")