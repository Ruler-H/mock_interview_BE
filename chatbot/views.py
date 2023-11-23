from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import ChatRoom
from .permissions import OnlyOwer
from .serializers import ChatRoomSerializer

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


chat_create = ChatCreateView.as_view()
chat_list = ChatListView.as_view()