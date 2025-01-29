# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('chat/<str:recipient_username>/', views.chat_room, name='chat_room'),
]