from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from libs.captcha.captcha import captcha
from verifications.serializers import RegisterSmsCodeSerializer
from . import constains
from random import randint

"""
图片验证码
"""


class RegisterImageCodeView(APIView):
    """
    生成图片验证码
    """

    def get(self, request, image_code_id):
        # 生成图片验证码内容和图片
        text, image = captcha.generate_captcha()
        # 链接redis
        redis_conn = get_redis_connection('code')
        # 存储图片验证码内容
        redis_conn.setex('img_%s' % image_code_id, constains.IMAGE_CODE_EXPIRE, text)
        print('image_code: ', text)

        # 将图片返回给前端,因为是图片格式,所以需要设置返回格式,不能直接使用Response,需要使用HttpResponse
        return HttpResponse(image, content_type='image/jpeg')


# 短信验证码
class RegisterSmsCodeView(APIView):
    """
    获取前段传递过来的图片验证码进行校验
    没有问题再生成短信验证码
    """

    def get(self, request,mobile):
        data = request.query_params  # 获取url中的请求参数
        serializer = RegisterSmsCodeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        # mobile = serializer.data.get('mobile')
        # 传递过来的数据验证没有问题,开始生成图片验证码
        sms_code = '%06d' % randint(0, 999999)

        # 判断该手机是否在1分钟之内发送过短信
        redis_conn = get_redis_connection('code')
        if redis_conn.get('sms_flag_%s' % mobile):
            return Response(status=status.HTTP_429_TOO_MANY_REQUESTS)
        # 将短信验证码存储进redis中
        redis_conn.setex('sms_%s' % mobile, constains.SMS_CODE_EXPIRE, sms_code)
        # 同时保存发送状态
        redis_conn.setex('sms_flag_%s' % mobile, constains.SMS_FLAG_EXPIRE, 1)
        print('sms_code:',sms_code)

        return Response({'message':'ok'})
