from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^imagecodes/(?P<image_code_id>.+)/$', views.RegisterImageCodeView.as_view())
]