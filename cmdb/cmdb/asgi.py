"""
ASGI config for cmdb project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from webssh.routing import websocket_urlpatterns
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cmdb.settings')

django_asgi_app = get_asgi_application()
application = ProtocolTypeRouter(
    {
    #http路由走这里
    "http":django_asgi_app,
    #chat应用下rountings模块下的路由变量socket_urlpatterns
    "websocket":AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(websocket_urlpatterns
                          ))
    )
    }
)