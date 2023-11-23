from django.db import models

class ChatRoom(models.Model):
    '''
    채팅방 모델
    '''
    client = models.ForeignKey(
        'account.User', 
        on_delete=models.CASCADE
    )
    
class ChatMessage(models.Model):
    '''
    채팅 메시지 모델
    '''
    chat_room = models.ForeignKey(
        'chatbot.ChatRoom',
        on_delete=models.CASCADE
    )
    content = models.TextField()
    # 0: client
    # 1: chatbot
    sender = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)