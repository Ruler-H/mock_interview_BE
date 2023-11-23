from rest_framework.permissions import BasePermission

class OnlyOwer(BasePermission):
    def has_object_permission(self, request, view, obj):
        '''
        모든 요청을 소유자만 허용하는 권한 제한 함수
        '''

        return obj.client == request.user