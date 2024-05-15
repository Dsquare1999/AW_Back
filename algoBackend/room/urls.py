from django.urls import path
from .views import RoomListCreateAPIView, MessageListCreateAPIView

urlpatterns = [
    path('rooms/', RoomListCreateAPIView.as_view(), name='room-list-create'),
    path('rooms/<int:room_id>/messages/', MessageListCreateAPIView.as_view(), name='message-list-create'),
]
