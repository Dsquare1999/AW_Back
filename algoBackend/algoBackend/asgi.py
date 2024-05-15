import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import room.routing as roomRouting
import chat.routing as chatRouting
import chat
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'algoBackend.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            roomRouting.websocket_urlpaterns,
        )
    )}
)