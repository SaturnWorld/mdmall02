from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User


class RegisterUsernameCountAPIView(APIView):
    """
    对接收到的用户名进行验证
    """
    def get(self,request,username):
        #获取用户个数
        count = User.objects.filter(username=username).count()

        context = {
            'count':count,
            'username':username
        }
        return Response(context)
