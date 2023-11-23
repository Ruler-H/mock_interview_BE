from rest_framework.serializers import ModelSerializer

from .models import ChatRoom, ChatMessage

class ChatRoomSerializer(ModelSerializer):
    '''
    채팅방 Serializer
    '''
    class Meta:
        model = ChatRoom
        fields = '__all__'

class ChatMessageSerializer(ModelSerializer):
    '''
    채팅 메시지 Serializer
    '''

    class Meta:
        model = ChatMessage
        fields = '__all__'