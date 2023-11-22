from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from django.contrib.auth import login, authenticate

from .serializers import UserSerializer, LoginSerializer

class UserCreateAPIView(CreateAPIView):
    '''
    사용자 생성 APIView
    '''
    serializer_class = UserSerializer


class LoginView(APIView):
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
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

signup = UserCreateAPIView.as_view()
login = LoginView.as_view()