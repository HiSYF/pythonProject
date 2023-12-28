# coding=utf-8
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer  # 自定义令牌(token)
from django.contrib.auth.backends import ModelBackend
#django的Q对象将SQL表达式封装在Python对象中，该对象可用于与数据库相关的操作。使用Q对象，我们可以使用更少和更简单的代码进行复杂查询。
from django.db.models import Q
from django.contrib.auth import get_user_model
# ⬇自定义令牌(token)
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # re_data = {}
        # re_data['data'] = data
        # re_data['code'] = 20000
        # re_data['message'] = 'success'

        return data
# ⬆自定义令牌(token)


User = get_user_model()

class MyCustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username) )
            if user.check_password(password):
                return user
        except Exception as e:
            return None
