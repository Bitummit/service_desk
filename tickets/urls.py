from django.urls import path
from tickets import views


urlpatterns = [
    path('issue/', views.IssueListView.as_view(), name="issue_list"),
    path('issue/<int:pk>', views.IssueUpdateView.as_view(), name="issue_update"),
    path('issue/<int:issue_id>/send_mail', views.SendMessageAPIView.as_view(), name="send_answer")
]