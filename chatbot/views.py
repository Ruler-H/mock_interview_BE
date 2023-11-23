from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import ChatCreateSerializer

class ChatCreateView(CreateAPIView):
    '''
    챗봇 채팅방 생성 view
    '''
    serializer_class = ChatCreateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


chat_create = ChatCreateView.as_view()