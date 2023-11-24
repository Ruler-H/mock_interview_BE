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

    def test_interview_grading(self):
        '''
        단위 문제 채점 기능 테스트
        '''
        print('-- 단위 문제 채점 기능 테스트 BEGIN --')
        response = self.client.post(
            '/interview/grading/',
            data={'question':'RESTful API를 설명하라.', 'answer':'RESTful API는 Representational State Transfer의 약자로 클라이언트와 서버간의 상호 운용을 위해 설계된 아키텍처 스타일이다. 이는 웹 서비스를 제공하고 관리하기 위한 소프트웨어의 디자인 원칙이며 간단하고 가벼 운 HTTP를 통해 자원을 전송하고 제어하는 방식을 사용한다.'},
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(response.data['score'], 0)
        self.assertLessEqual(response.data['score'], 10)
        print('-- 단위 문제 채점 기능 테스트 END --')
