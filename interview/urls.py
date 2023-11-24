from django.urls import path, include
from . import views

app_name = 'interview'

urlpatterns = [
    path('question/', views.question, name='quetion'),
    path('grading/', views.grading, name='grading'),
]