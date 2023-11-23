from django.db import models

class ChatRoom(models.Model):
    client = models.ForeignKey(
        'account.User', 
        on_delete=models.CASCADE
    )
    
class ChatMessage(models.Model):
    chat_room = models.ForeignKey(
        'chatbot.ChatRoom',
        on_delete=models.CASCADE
    )
    content = models.TextField()
    sender = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)