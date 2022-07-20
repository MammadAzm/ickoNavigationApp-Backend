from channels.routing import ProtocolTypeRouter , URLRouter
from channels.auth import AuthMiddlewareStack

from django.urls import path

from ickoNavigator.consumer import *


websocket_urlPattern = [
    path('update/', UpdateData),
]




application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(URLRouter(websocket_urlPattern)),
})
