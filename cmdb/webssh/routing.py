from django.urls import re_path

from . import LogsConsumers,SSHConsumers

# 这个变量是存放websocket的路由Ï
websocket_urlpatterns = [
    re_path(r"ws/message/(?P<username>[\w+|\-?]+)+/(?P<token>\w+)$", LogsConsumers.RobotMessageConsumer.as_asgi()),
    re_path(r'ws/ssh/(?P<id>\w+)', SSHConsumers.SSHConsumer.as_asgi()),
    re_path(r'^ws/ssh/$', SSHConsumers.SSHConsumer.as_asgi()),
]