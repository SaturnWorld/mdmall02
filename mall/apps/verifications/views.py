from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework.views import APIView
from libs.captcha.captcha import captcha
from . import constains


class RegisterImageCodeView(APIView):
    """
    生成图片验证码
    """
    def get(self,request,image_code_id):
        #生成图片验证码内容和图片
        text,image = captcha.generate_captcha()
        #链接redis
        redis_conn = get_redis_connection('code')
        #存储图片验证码内容
        redis_conn.setex('img_%s'%image_code_id,constains.IMAGE_CODE_EXPIRE,text)
        print('image_code: ',text)

        #将图片返回给前端,因为是图片格式,所以需要设置返回格式,不能直接使用Response,需要使用HttpResponse
        return HttpResponse(image,content_type='image/jpeg')

