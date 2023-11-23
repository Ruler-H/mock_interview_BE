from django.test import TestCase
from rest_framework.test import APIClient

from .models import ChatRoom
from account.models import User

class TestChatbot(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.post(
            '/account/signup/', 
            {'email': 'test@gmail.com', 'username': 'test', 'password': 'testtest1@', 'password2': 'testtest1@'}, 
            format='json')
        
        response = self.client.post(
            '/account/login/', 
            {'email': 'test@gmail.com', 'password': 'testtest1@'})
        self.access_token = response.data['access']

    def test_chatbot_create(self):
        '''
        챗봇 생성 테스트
        '''
        print('-- 챗봇 생성 테스트 BEGIN --')
        user = User.objects.get(pk=1)

        # 권한 없이 요청하는 경우 401
        response = self.client.post(
            '/chatbot/',)
        self.assertEqual(response.status_code, 401)

        # 권한이 있는 사용자가 요청하는 경우 201
        response = self.client.post(
            '/chatbot/', 
            data={'client':1},
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            format='json')
        self.assertEqual(response.status_code, 201)

        self.assertEqual(ChatRoom.objects.get(pk=1).client.username, 'test')

        self.assertEqual(ChatRoom.objects.all().count(), 1)
        print('-- 챗봇 생성 테스트 END --')