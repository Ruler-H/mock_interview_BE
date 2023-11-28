from rest_framework.throttling import SimpleRateThrottle

class UserRateThrottle(SimpleRateThrottle):
    rate = '5/day'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            return self.cache_format % {
                'scope': self.scope,
                'ident': request.user.pk  # 유저 별로 요청 횟수를 추적하기 위해 User의 primary key를 사용
            }