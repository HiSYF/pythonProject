from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
# coding=utf-8
from django.contrib.auth.backends import ModelBackend
#django的Q对象将SQL表达式封装在Python对象中，该对象可用于与数据库相关的操作。使用Q对象，我们可以使用更少和更简单的代码进行复杂查询。
from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework_simplejwt import authentication
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
from cmdb import settings
import base64
from rest_framework_simplejwt.views import TokenObtainPairView # 自定义视图
from rest_framework.permissions import AllowAny # 自定义视图
from .serializers import MyTokenObtainPairSerializer # 自定义视图
# ⬇自定义视图
class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
# ⬆自定义视图

from rest_framework.views import APIView


User = get_user_model()

class MyCustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        private_key = settings.private_key
        pri_key = RSA.importKey(private_key)
        cipher = PKCS1_cipher.new(pri_key)
        password_bs64 = base64.b64decode(password)
        back_text = cipher.decrypt(password_bs64, None)
        password_encode = back_text.decode('utf-8')
        try:
            user = User.objects.get(Q(username=username) | Q(email=username) )
            if user.check_password(password_encode):
                return user
        except Exception as e:
            return None
