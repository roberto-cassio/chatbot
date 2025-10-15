from django.urls import path, include
from .views import ChatView

urlpatterns = [
    path('question-and-answer/', ChatView, name='chat'),
]