# coding=utf-8
from django.http import JsonResponse, HttpResponse
# Create your views here.
from .models import UserProfile
from django.contrib.auth import get_user_model
from rest_framework_simplejwt import authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from cmdb import settings

class ArticleUserInfo(APIView):
    # User = get_user_model()
    def get(self,request):
        # 获取请求参数token的值
        token = request.headers.get('AUTHORIZATION')
        token = token.replace('JWT ', '')
        token_msg = authentication.JWTAuthentication().get_validated_token(token)
        user_object = authentication.JWTAuthentication().get_user(token_msg)
        # print(user_object)
        data = {"username": user_object.username,
                "first_name": user_object.first_name,
                "last_name": user_object.last_name,
                "avatar": user_object.avatar,
                #  "groups":user_object.groups,
                "roles": user_object.role,
                "introduction": user_object.introduction
                }
        # re_data = {"data": data,
        #            "code": 20000,
        #            "message": "success"
        #            }
        return Response(data)

def getPubKey(request):
    pubKey = settings.public_key
    re_data = {}
    re_data['data'] = pubKey.decode('utf-8')
    re_data['code'] = 200
    re_data['message'] = 'success'
    # pubKey = pubKey.replace("-----BEGIN PUBLIC KEY-----", "")
    # pubKey = pubKey.replace("-----END PUBLIC KEY-----", "")
    return JsonResponse(re_data)
