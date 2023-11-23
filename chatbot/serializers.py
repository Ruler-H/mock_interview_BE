from rest_framework.serializers import ModelSerializer

from .models import ChatRoom

class ChatRoomSerializer(ModelSerializer):
    '''
    Chat Serializer
    '''
    class Meta:
        model = ChatRoom
        fields = '__all__'