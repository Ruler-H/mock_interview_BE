from django.test import TestCase
from rest_framework.test import APIClient

class TestInterview(TestCase):
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

    def test_interview_question(self):
        '''
        면접 질문 요청 기능 테스트
        '''
        print('-- 면접 질문 요청 기능 테스트 BEGIN --')
        response = self.client.post(
            '/interview/question/',
            data={'career':'junior', 'field':'backend'},
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data['question_list']), 10)
        print('-- 면접 질문 요청 기능 테스트 END --')
