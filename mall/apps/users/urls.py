from django.conf.urls import url
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    #/users/usernames/(?P<username>\w{5,20})/count/
    url(r'^usernames/(?P<username>\w{5,20})/count/$',views.RegisterUsernameCountAPIView.as_view(),name='usernamecount'),
    url(r'^phones/(?P<mobile>1[3456789]\d{9})/count/$',views.RegisterPhoneCountAPIView.as_view(),name='phonecount'),
    #注册
    url(r'^$',views.RegisterCreateAPIView.as_view()),
    #登陆
    url(r'^auths/',obtain_jwt_token,name='auths')

]