from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'interview'

router = DefaultRouter()
router.register('favorite', views.FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('question/', views.question, name='quetion'),
    path('grading/', views.grading, name='grading'),
    path('total_grading/', views.total_grading, name='total_grading'),
    path('', include(router.urls)),
]