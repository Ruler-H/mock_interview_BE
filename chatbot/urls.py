from django.urls import path, include
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chat_create, name='chat_create'),
]