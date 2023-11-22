from datetime import datetime, timedelta, timezone
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken, Token
from rest_framework_simplejwt.exceptions import TokenError

from .models import User

class TestAccount(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_account_signup(self):
        '''
        회원가입 테스트
        비밀번호 유효성 요구사항
            - 8글자 이상 15글자 이하
            - 숫자, 특수문자 포함
            - 확인 비밀번호와 일치
        '''
        print('-- 회원가입 테스트 BEGIN --')
        # 비밀번호 유효성 테스트 - 8글자 이상
        response = self.client.post(
            '/account/signup/', 
            {'email': 'elwl5515@gmail.com', 'username': 'hwang', 'password': 'test1@', 'password2': 'test1@'}, 
            format='json')
        self.assertEqual(response.status_code, 400)

        # 비밀번호 유효성 테스트 - 15글자 이하
        response = self.client.post(
            '/account/signup/', 
            {'email': 'elwl5515@gmail.com', 'username': 'hwang', 'password': 'testtesttesttest1@', 'password2': 'testtesttesttest1@'}, 
            format='json')
        self.assertEqual(response.status_code, 400)

        # 비밀번호 유효성 테스트 - 숫자, 특수문자 포함
        response = self.client.post(
            '/account/signup/', 
            {'email': 'elwl5515@gmail.com', 'username': 'hwang', 'password': 'testtest', 'password2': 'testtest'}, 
            format='json')
        self.assertEqual(response.status_code, 400)

        # 비밀번호 유효성 테스트 - 확인 비밀번호와 일치
        response = self.client.post(
            '/account/signup/', 
            {'email': 'elwl5515@gmail.com', 'username': 'hwang', 'password': 'testtest1@', 'password2': 'testtest!2'}, 
            format='json')
        self.assertEqual(response.status_code, 400)

        # 회원가입 테스트
        response = self.client.post(
            '/account/signup/', 
            {'email': 'test@gmail.com', 'username': 'test', 'password': 'testtest1@', 'password2': 'testtest1@'}, 
            format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get(id=1).email, 'test@gmail.com')
        self.assertEqual(User.objects.get(id=1).username, 'test')

        print('-- 회원가입 테스트 END --')

    def test_account_login(self):
        '''
        로그인 테스트
        '''
        print('-- 로그인 테스트 BEGIN --')
        self.client.post(
            '/account/signup/', 
            {'email': 'test@gmail.com', 'username': 'test', 'password': 'testtest1@', 'password2': 'testtest1@'}, 
            format='json')
        
        # 로그인 실패 테스트 - 비밀번호를 틀린 경우
        response = self.client.post(
            '/account/login/',
            {'email': 'test@gmail.com', 'password':'testtest2!'},
            format='json'
        )
        self.assertIn(response.status_code, [400, 401])

        # 로그인 실패 테스트 - 이메일이 없는 경우
        response = self.client.post(
            '/account/login/',
            {'email': '', 'password':'testtest2!'},
            format='json'
        )
        self.assertIn(response.status_code, [400, 401])

        # 로그인 실패 테스트 - 비밀번호가 없는 경우
        response = self.client.post(
            '/account/login/',
            {'email': 'test@gmail.com', 'password':'testtest2!'},
            format='json'
        )
        self.assertIn(response.status_code, [400, 401])

        # 로그인 성공 테스트
        response = self.client.post(
            '/account/login/',
            {'email': 'test@gmail.com', 'password':'testtest1@'},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['refresh'])
        self.assertTrue(response.data['access'])
        logged_in = self.client.login(email='test@gmail.com', password='testtest1@')
        self.assertTrue(logged_in)
        print('-- 로그인 테스트 END --')

    def test_token_expiration(self):
        '''
        JWT token 만료 테스트
        '''
        print('-- JWT token 만료 테스트 BEGIN --')
        user = User.objects.create_user(email='test@test.com', password='testtest1@')
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token

        refresh_exp = datetime.now() + timedelta(hours=2)
        access_exp = datetime.now() + timedelta(minutes=30)
        
        refresh_token = refresh_token.set_exp(refresh_exp)
        access_token = access_token.set_exp(access_exp)

        refresh_token = str(refresh_token)
        access_token = str(access_token)

        try:
            RefreshToken(refresh_token)
            is_valid = True
        except:
            is_valid = False
        self.assertFalse(is_valid)
    
        try:
            RefreshToken(access_token)
            is_valid = True
        except:
            is_valid = False
        self.assertFalse(is_valid)

        print('-- JWT token 만료 테스트 END --')

    # def test_account_logout(self):
    #     '''
    #     로그아웃 테스트
    #     '''
    #     print('-- 로그아웃 테스트 BEGIN --')
    #     self.client.post(
    #         '/account/login/',
    #         {'email': 'test@gmail.com', 'password':'testtest1@'},
    #         format='json'
    #     )
    #     response = self.client.get('/account/logout/')
    #     self.assertEqual(response.status_code, 200)
    #     print('-- 로그아웃 테스트 END --')