from rest_framework.serializers import ModelSerializer

from .models import Favorite

class FavoriteSerializer(ModelSerializer):
    '''
    즐겨찾기 Serializer
    '''
    class Meta:
        model = Favorite
        fields = '__all__'