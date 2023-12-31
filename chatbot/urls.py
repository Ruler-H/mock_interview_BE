from django.urls import path, include

from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chat_create, name='chat_create'),
    path('list/', views.chat_list, name='chat_list'),
    path('answer/', views.chat_answer, name='chat_answer'),
    path('<int:pk>/messages/', views.chat_messages, name='chat_messages'),
    path('<int:pk>/', views.chat_delete, name='chat_delete'),
]