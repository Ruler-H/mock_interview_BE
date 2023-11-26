from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = 'account'

router = DefaultRouter()
router.register('user', views.UserViewSet, basename='user')

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('', include(router.urls)),
    path('status/', views.account_status, name='status'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]