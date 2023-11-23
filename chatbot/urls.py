from django.urls import path, include
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chat_create, name='chat_create'),
    path('list/', views.chat_list, name='chat_list'),
]