from django.test import TestCase
from rest_framework.test import APIClient

from .models import Favorite

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

    def test_interview_total_grading(self):
        '''
        모의 면접 전체 채점 기능 테스트
        '''
        print('-- 모의 면접 전체 채점 기능 테스트 BEGIN --')
        response = self.client.post(
            '/interview/total_grading/',
            data={
                'question_list':[
                    {'question':'HTTP 프로토콜 메시지의 구조는 무엇이고 어떤 용도로 사용됩니까?',
                    'answer':'HTTP 프로토콜 메시지는 헤더 및 바디 두 가지 요소로 구성되어 있습니다. 헤더는 요청과 응답의 정보를 포함하고 있고 바디는 요청 또는 응답과 관련한 데이터를 포함하고 있습니다. HTTP 프로토콜은 웹 서버와 클라이언트 사이의 요청과 응답의 정보를 주고 받기 위해 사용됩니다.'},
                    {'question':'메모리 관리란 무엇인가요?',
                    'answer':'HTTP 요청과 응답은 각각 헤더 바디 상태 라인 등의 요소로 구성되어 있습니다.'},
                ]
            },
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(response.data['score'], 0)
        self.assertLessEqual(response.data['score'], 10)
        self.assertTrue(response.data['complement'])
        print('-- 모의 면접 전체 채점 기능 테스트 END --')

    def test_interview_favorite_add(self):
        '''
        즐겨찾기 추가 기능 테스트
        '''
        print('-- 즐겨찾기 추가 기능 테스트 BEGIN --')
        response = self.client.post(
            '/interview/favorite/',
            data={
                'grade':'하',
                'field':'BE',
                'question':'HTTP 프로토콜 메시지의 구조는 무엇이고 어떤 용도로 사용됩니까?',
                'intent':'HTTP에 대한 이해',
                'model_answer':'HTTP 프로토콜 메시지는 헤더 및 바디 두 가지 요소로 구성되어 있습니다. 헤더는 요청과 응답의 정보를 포함하고 있고 바디는 요청 또는 응답과 관련한 데이터를 포함하고 있습니다. HTTP 프로토콜은 웹 서버와 클라이언트 사이의 요청과 응답의 정보를 주고 받기 위해 사용됩니다.'
            },
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Favorite.objects.all().count(), 1)
        print('-- 즐겨찾기 추가 기능 테스트 END --')

    def test_interview_favorite_delete(self):
        '''
        즐겨찾기 삭제 기능 테스트
        '''
        print('-- 즐겨찾기 삭제 기능 테스트 BEGIN --')
        self.client.post(
            '/interview/favorite/',
            data={
                'grade':'하',
                'field':'BE',
                'question':'HTTP 프로토콜 메시지의 구조는 무엇이고 어떤 용도로 사용됩니까?',
                'intent':'HTTP에 대한 이해',
                'model_answer':'HTTP 프로토콜 메시지는 헤더 및 바디 두 가지 요소로 구성되어 있습니다. 헤더는 요청과 응답의 정보를 포함하고 있고 바디는 요청 또는 응답과 관련한 데이터를 포함하고 있습니다. HTTP 프로토콜은 웹 서버와 클라이언트 사이의 요청과 응답의 정보를 주고 받기 위해 사용됩니다.'
            },
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            format='json'
        )
        response = self.client.delete(
            '/interview/favorite/1/',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Favorite.objects.all().count(), 0)
        print('-- 즐겨찾기 삭제 기능 테스트 END --')

    def test_interview_field_question(self):
        '''
        분야별 질문 요청 기능 테스트
        '''
        print('-- 분야별 질문 요청 기능 테스트 BEGIN --')
        response = self.client.post(
            '/interview/field_question/',
            data={
                'field':'BE',
            },
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data['question_list']), 2)
        print('-- 분야별 질문 요청 기능 테스트 END --')


    def test_interview_favorite_list(self):
        '''
        즐겨찾기 목록 기능 테스트
        '''
        print('-- 즐겨찾기 목록 기능 테스트 BEGIN --')
        self.client.post(
            '/interview/favorite/',
            data={
                'grade':'하',
                'field':'BE',
                'question':'HTTP 프로토콜 메시지의 구조는 무엇이고 어떤 용도로 사용됩니까?',
                'intent':'HTTP에 대한 이해',
                'model_answer':'HTTP 프로토콜 메시지는 헤더 및 바디 두 가지 요소로 구성되어 있습니다. 헤더는 요청과 응답의 정보를 포함하고 있고 바디는 요청 또는 응답과 관련한 데이터를 포함하고 있습니다. HTTP 프로토콜은 웹 서버와 클라이언트 사이의 요청과 응답의 정보를 주고 받기 위해 사용됩니다.'
            },
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            format='json'
        )
        self.client.post(
            '/interview/favorite/',
            data={
                'grade':'하',
                'field':'BE',
                'question':'HTTP 프로토콜 메시지의 구조는 무엇이고 어떤 용도로 사용됩니까?',
                'intent':'HTTP에 대한 이해',
                'model_answer':'HTTP 프로토콜 메시지는 헤더 및 바디 두 가지 요소로 구성되어 있습니다. 헤더는 요청과 응답의 정보를 포함하고 있고 바디는 요청 또는 응답과 관련한 데이터를 포함하고 있습니다. HTTP 프로토콜은 웹 서버와 클라이언트 사이의 요청과 응답의 정보를 주고 받기 위해 사용됩니다.'
            },
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            format='json'
        )
        self.client.post(
            '/interview/favorite/',
            data={
                'grade':'하',
                'field':'BE',
                'question':'HTTP 프로토콜 메시지의 구조는 무엇이고 어떤 용도로 사용됩니까?',
                'intent':'HTTP에 대한 이해',
                'model_answer':'HTTP 프로토콜 메시지는 헤더 및 바디 두 가지 요소로 구성되어 있습니다. 헤더는 요청과 응답의 정보를 포함하고 있고 바디는 요청 또는 응답과 관련한 데이터를 포함하고 있습니다. HTTP 프로토콜은 웹 서버와 클라이언트 사이의 요청과 응답의 정보를 주고 받기 위해 사용됩니다.'
            },
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            format='json'
        )
        self.client.post(
            '/interview/favorite/',
            data={
                'grade':'하',
                'field':'BE',
                'question':'HTTP 프로토콜 메시지의 구조는 무엇이고 어떤 용도로 사용됩니까?',
                'intent':'HTTP에 대한 이해',
                'model_answer':'HTTP 프로토콜 메시지는 헤더 및 바디 두 가지 요소로 구성되어 있습니다. 헤더는 요청과 응답의 정보를 포함하고 있고 바디는 요청 또는 응답과 관련한 데이터를 포함하고 있습니다. HTTP 프로토콜은 웹 서버와 클라이언트 사이의 요청과 응답의 정보를 주고 받기 위해 사용됩니다.'
            },
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            format='json'
        )
        response = self.client.get(
            '/interview/favorite/',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Favorite.objects.all().count(), 4)
        print('-- 즐겨찾기 목록 기능 테스트 END --')