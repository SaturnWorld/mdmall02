from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import RegisterCreateSerializer


class RegisterUsernameCountAPIView(APIView):
    """
    用户输完用户名之后,移出焦点前段即传递用户名到后端校验
    后端从数据库校验用户名是否已注册过,再返回
    ^usernames/(?P<username>\w{5,20})/count/$
    """
    def get(self,request,username):
        #获取用户个数
        count = User.objects.filter(username=username).count()

        context = {
            'count':count,
            'username':username
        }
        return Response(context)

class RegisterPhoneCountAPIView(APIView):
    """
    用户输入手机号之后前段将手机号码传递到后端,后端接收到之后,
    从数据库查询是否已注册过
    GET :phones/(?P<mobile>1[3456789]\d{9}/count/)
    """
    def get(self,request,mobile):
        count = User.objects.filter(mobile=mobile).count()

        context = {
            'count':count,
            'mobile':mobile
        }
        return Response(context)

#注册
class RegisterCreateAPIView(CreateAPIView):
    """
    CreateAPIView
    提供 post 方法
    继承自： GenericAPIView、CreateModelMixin
    """
    serializer_class = RegisterCreateSerializer
