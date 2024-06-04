from rest_framework import serializers
from .models import Room, Message
from django.contrib.auth.models import User

from accounts.serializers import MinimalUserSerializer

class RoomSerializer(serializers.ModelSerializer):
    participants = MinimalUserSerializer(read_only=True, many=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Room
        exclude = ['deleted', 'created_at', 'updated_at']

    def get_messages(self, instance):
        try:
            messages = instance.messages.filter(deleted=False)
            room_messages = MessageSerializer(instance=messages, many=True)
            return room_messages.data
        except Exception as e:
            return None

class MessageSerializer(serializers.ModelSerializer):
    user = MinimalUserSerializer(read_only=True)

    class Meta:
        model = Message
        exclude = ['id', 'deleted', 'updated_at']

    def validate_room(self, value):
        if not Room.objects.filter(id=value).exists():
            raise serializers.ValidationError("Room does not exist")
        return value
    
    def validate_user(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User does not exist")
        return value