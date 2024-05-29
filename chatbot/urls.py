# chatbot/urls.py

from django.urls import path
from .views import RegisterView, LoginView, chat, conversation_history

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('chat/', chat, name='chat'),
    path('history/<str:username>/', conversation_history, name='conversation_history'),
]
