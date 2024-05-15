# import imp
from django.urls import path
from . import consumers

websocket_urlpaterns = [
    path('ws/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
]