from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from django.contrib.auth import authenticate

from .models import User

class UserSerializer(ModelSerializer):
    '''
    사용자 Serializer
    '''
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password':{'write_only': True}
        }

    def create(self, validated_data):
        '''
        사용자 유효성 검사 후 사용자 생성하는 함수
        '''
        password = validated_data.pop('password')
        user = User(
            email=validated_data.pop('email'),
            username=validated_data.pop('username'))
        user.set_password(password)
        user.save()
        return user
    
    def validate(self, data):
        '''
        패스워드의 유효성을 검증하는 함수
            - 길이 : 8글자 이상 15글자 이하
            - 포함 : 숫자, 특수문자
            - 확인 비밀번호와의 일치
        '''
        password = data.get('password')
        if len(password) < 8 or len(password) > 15:
            raise serializers.ValidationError("비밀번호는 8글자 이상, 15글자 이하이어야 합니다.")
        
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError("비밀번호는 숫자를 포함해야 합니다.")
        
        if not any(char in '!@#$%^&*()_+' for char in password):
            raise serializers.ValidationError("비밀번호는 특수문자를 포함해야 합니다.")
        
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        return data
    
class LoginSerializer(Serializer):
    '''
    로그인 Serializer
    '''
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        '''
        로그인 유효성 검사 함수
            - 이메일 입력 여부
            - 비밀번호 입력 여부
            - 이메일, 비밀번호 일치 여부
        '''
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if user:
                return data
            else:
                raise serializers.ValidationError('이메일 혹은 비밀번호가 틀립니다.')
        else:
            raise serializers.ValidationError('이메일과 비밀번호를 모두 입력하셔야 합니다.')


