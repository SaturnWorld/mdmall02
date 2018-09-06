import re

from django.contrib.auth.backends import ModelBackend

from users.models import User


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }


def get_user_by_acount(acount):
    try:
        if re.match(r'1[345789]\d{9}', acount):
            user = User.objects.get(mobile=acount)
        else:
            user = User.objects.get(username=acount)
    except User.DoseNotExist:
        user = None

    return user

#自定义登陆认证继承ModelBackend,并重写authenticate方法
class UsernameMobileAuthBackend(ModelBackend):
    """
    自定义用户可以以手机当做用户名进行登陆
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_by_acount(username)
        if user is not None and user.check_password(password):
            return user


