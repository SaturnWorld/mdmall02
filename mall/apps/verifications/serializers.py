from django_redis import get_redis_connection
from rest_framework.views import APIView
from rest_framework import serializers


class RegisterSmsCodeSerializer(serializers.Serializer):
    """
    校验验证码内容和image_code_id(uuid)
    """
    # required:表示反序列化时必须要输入,默认为true
    text = serializers.CharField(label='验证码', max_length=4, min_length=4, required=True)
    image_code_id = serializers.UUIDField(label='验证码唯一id')

    # 定义校验函数,因为要校验text必须要使用image_code_id,所以属于是多字段的校验
    def validate(self, attrs):
        # 获取uuid
        image_code_id = attrs['image_code_id']
        # 链接redis获取存储在redis中的验证码内容
        redis_conn = get_redis_connection('code')
        # 获取redis中的验证码内容
        redis_text = redis_conn.get('img_%s' % image_code_id)
        if redis_text is None:
            raise serializers.ValidationError('图片验证码已过期')
        # 获取用户传递过来的验证码内容
        text = attrs['text']
        if text.lower() != redis_text.decode().lower():
            raise serializers.ValidationError('图片验证码有误')
        return attrs