from rest_framework.serializers import ModelSerializer

from .models import ChatRoom

class ChatCreateSerializer(ModelSerializer):
    '''
    Chat 생성 Serializer
    '''
    class Meta:
        model = ChatRoom
        fields = '__all__'