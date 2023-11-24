from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from .models import Favorite
from .serializers import FavoriteSerializer
from .utils import generate_score, generate_question, generate_total_score

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def question(request):
    '''
    모의 면접을 위한 문제 요청(POST) view 함수
    '''
    career = request.data['career']
    field = request.data['field']
    data = f'system: assistant는 {career} {field} 기술 면접 전문가이다.'
    data += f'\nuser: {career} {field} 기술 면접 예시 질문을 질문, 모범 답변, 질문 의도, 질문 난이도로 정리해서 한글로 답해줘. 질문 난이도는 상, 중, 하로 답변해주고, 오직 json 형태로만 응답주고, key 값으로는 question, answer, intent, difficulty로 응답해줘.'
    question_list = generate_question(data, 10)
    
    return Response(data={'question_list':question_list}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def grading(request):
    '''
    모의 면접 중 단위 문제 채점(POST) view 함수
    '''
    question = request.data['question']
    answer = request.data['answer']
    data = f'system: assistant는 developer 기술 면접 전문가이다.'
    data += f'\nuser: {question}라는 질문에 {answer}라고 답하면 10점 만점에 몇점인지 숫자만 알려줘'
    score = generate_score(data)
    return Response(data={'score':score}, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def total_grading(request):
    '''
    모의 면접 전체 채점(POST) view 함수
    '''
    data = f'system: assistant는 developer 기술 면접 전문가이다.'
    question_list = request.data['question_list']
    user = ''
    for question in question_list:
        q = question['question']
        a = question['answer']
        user += f'{q}라는 질문에 {a}라고 답하고 '
    user = user[:-4]
    data += f'\nuser: {user}답하면 10점 만점에 몇점인지, 보완점은 무엇인지 답해줘. 오직 json 형태로만 응답주고, key 값으로는 score, complement로 응답해줘.'
    score, complement = generate_total_score(data)
    return Response(data={'score':score, 'complement':complement}, status=status.HTTP_200_OK)

class FavoriteViewSet(ModelViewSet):
    '''
    즐겨찾기를 추가, 삭제하는 ViewSet
    '''
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        '''
        즐겨찾기 추가 함수
        '''
        request.data['user'] = request.user.pk
        serializer = FavoriteSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        '''
        즐겨찾기 삭제 함수
        '''
        favorite = Favorite.objects.get(pk=pk)

        # 본인 확인
        if request.user != favorite.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        # 즐겨찾기 삭제
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def field_question(request):
    '''
    모의 면접을 위한 문제 요청(POST) view 함수
    '''
    field = request.data['field']
    data = f'system: assistant는 {field} 기술 면접 전문가이다.'
    data += f'\nuser: {field} 기술 면접 예시 질문을 질문, 모범 답변, 질문 의도, 질문 난이도로 정리해서 한글로 답해줘. 질문 난이도는 상, 중, 하로 답변해주고, 오직 json 형태로만 응답주고, key 값으로는 question, answer, intent, difficulty로 응답해줘.'
    question_list = generate_question(data, 2)
    return Response(data={'question_list':question_list}, status=status.HTTP_201_CREATED)