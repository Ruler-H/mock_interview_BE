import requests
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .utils import generate_text
from .permissions import OnlyOwer
from .models import ChatRoom, ChatMessage
from .serializers import ChatRoomSerializer, ChatMessageSerializer

class ChatCreateView(CreateAPIView):
    '''
    챗봇 채팅방 생성 view
    '''
    serializer_class = ChatRoomSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class ChatListView(ListAPIView):
    serializer_class = ChatRoomSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, OnlyOwer]

    def get_queryset(self):
        return ChatRoom.objects.filter(client=self.request.user)


class ChatAnswerView(APIView):
    '''
    채팅 답변 요청 view
    '''
    serializer_class = ChatMessageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, OnlyOwer]

    def post(self, request):
        '''
        챗봇 답변 요청 처리(POST) 함수
        '''
        question = request.data['question']
        if not question.strip():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        chat_room = ChatRoom.objects.get(pk=request.data['room_pk'])
        ChatMessage.objects.create(chat_room=chat_room, content=question, sender=False).save()
        
        data = 'system: assistant는 백엔드 기술 면접 전문가이다.'

        messages = ChatRoom.objects.prefetch_related('chatmessage_set').get(pk=request.data['room_pk']).chatmessage_set.all()
        for message in messages:
            role = 'user'
            if message.sender:
                role = 'assistant'
            data += f'\n{role}: {message.content}'
        answer = generate_text(data)
        answer = answer.split(':')[-1].strip()
        ChatMessage.objects.create(chat_room=chat_room, content=answer, sender=True).save()

        return Response(data={'answer':answer}, status=status.HTTP_201_CREATED)


class ChatMessageListView(ListAPIView):
    serializer_class = ChatMessageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, OnlyOwer]
    queryset = ChatMessage.objects.all()
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = self.queryset.filter(chat_room__id=pk)
        print(queryset)
        return queryset


chat_create = ChatCreateView.as_view()
chat_list = ChatListView.as_view()
chat_answer = ChatAnswerView.as_view()
chat_messages = ChatMessageListView.as_view()