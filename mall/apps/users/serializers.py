import re

from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework.settings import api_settings

from users.models import User


class RegisterCreateSerializer(serializers.ModelSerializer):
    """
    POST请求传递过来的数据有
    username,
    password,
    password2,
    mobile,
    sms_code,
    allow
    """
    # password2,sms_code,allow三个属性在User表中没有定义,需要加上这三个字段的定义

    password2 = serializers.CharField(label='校验密码', allow_null=False, allow_blank=False, write_only=True)
    sms_code = serializers.CharField(label='短信验证码', max_length=6, min_length=6, allow_null=False, allow_blank=False,
                                     write_only=True)
    allow = serializers.CharField(label='是否同意协议', allow_null=False, allow_blank=False, write_only=True)

    #增加JWT的token字段
    token = serializers.CharField(label='登录状态token', read_only=True)  # 增加token字段

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'mobile', 'password2', 'sms_code', 'allow','token')
        # 额外添加的字段定义,有验证的作用
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    # 定义方法对字段进行验证
    def validate_mobile(self, value):
        if not re.match(r'1[345789]\d{9}', value):
            raise serializers.ValidationError('手机号码格式错误')
        return value

    def validate_allow(self, value):
        if not value:
            raise serializers.ValidationError('您还没有同意协议')
        return value

    # 多字段验证:密码,短信验证码
    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs['password2']
        if password != password2:
            raise serializers.ValidationError('两次输入的密码不一致')

        # 验证短信验证码
        redis_conn = get_redis_connection('code')
        mobile = attrs['mobile']
        redis_sms_code = redis_conn.get('sms_%s' % mobile)
        if redis_sms_code is None:
            raise serializers.ValidationError('短信验证码已过期')
        sms_coed = attrs['sms_code']
        if int(redis_sms_code.decode()) != int(sms_coed):
            raise serializers.ValidationError('短信验证码错误')

        return attrs

    #进行数据存储
    def create(self, validated_data):
        #因为password2,sms_code,allow三个数据不需要入库,所以要将这三个数据先删掉
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']

        #创建用户
        user = super().create(validated_data)

        #密码要进行加密再存入数据库
        user.set_password(validated_data['password'])
        user.save()

        #补充生成记录登陆状态的token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token

        return user
