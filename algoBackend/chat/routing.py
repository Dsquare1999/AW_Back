from django.urls import path
from . import consumers

websocket_urlpaterns = [
    path('uws/', consumers.UserChatConsumer.as_asgi()),
]