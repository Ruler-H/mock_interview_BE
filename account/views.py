from datetime import timedelta
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .serializers import UserSerializer, LoginSerializer

class UserCreateAPIView(CreateAPIView):
    '''
    사용자 생성 APIView
    '''
    serializer_class = UserSerializer


class LoginView(TokenObtainPairView):
    '''
    로그인 APIView
    '''
    def post(self, request):
        '''
        로그인 요청(POST) 처리 함수
        '''
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request,
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'])
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    

class LogoutView(APIView):
    '''
    로그아웃 APIView
    '''
    def post(self, request):
        try:
            refresh_token = RefreshToken(request.data["refresh"])
            refresh_token.set_exp(timedelta(days=1))
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


signup = UserCreateAPIView.as_view()
login = LoginView.as_view()
logout = LogoutView.as_view()