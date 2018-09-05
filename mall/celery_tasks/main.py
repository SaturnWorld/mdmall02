"""
celery的启动文件
"""
from celery import Celery

#创建celery对象
#参数main,设置脚本名
app = Celery('celery_tasks')

#加载配置文件
app.config_from_object('celery_tasks.config')

#自动加载任务
app.autodiscover_tasks(['celery_tasks.sms'])

#启动celery:
#celery -A celery_tasks.main worker -l info