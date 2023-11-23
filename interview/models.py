from django.db import models

class Favorite(models.Model):
    '''
    즐겨찾기 모델
    '''
    grade = models.CharField(max_length=50)
    field = models.CharField(max_length=50)
    question = models.CharField(max_length=200)
    intent = models.TextField()
    model_answer = models.TextField()
    user = models.ForeignKey(
        'account.User', 
        on_delete=models.CASCADE
    )