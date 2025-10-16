from django.urls import path, include
from .views import chat_view

urlpatterns = [
    path('question-and-answer/', chat_view, name='chat'),
]