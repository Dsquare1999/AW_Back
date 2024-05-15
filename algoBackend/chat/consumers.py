import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from accounts.models import User

class UserChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):

        if self.scope["user"].is_anonymous:
            self.authenticated_user_chat_room = f'user_chat_anonymous'
            self.close()

        else:
            authenticatedUser = self.scope["user"].id
            self.authenticated_user_chat_room = f'user_chat_{authenticatedUser}'
            
            await self.channel_layer.group_add(
                self.authenticated_user_chat_room,
                self.channel_name
            )
            await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.authenticated_user_chat_room,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        sent_by_user = data['sent_by_user']
        sent_to_user = data['sent_to_user']

        if not message:
            print('Error:: empty message')
            return False
            
        sent_by_user = await self.get_user_object(sent_by_user)
        sent_to_user = await self.get_user_object(sent_to_user)

        if not sent_by_user:
            print('Error:: sent by user is incorrect')
        if not sent_to_user:
            print('Error:: send to user is incorrect')

        await self.channel_layer.group_send(
            self.authenticated_user_chat_room,
            {
                'type': 'receive_group_message',
                'message': message,
                'username': username,
                'sent_by_user': sent_by_user,
                'sent_to_user': sent_to_user,
            }
        )
        
        self.other_user_chat_room = f'user_chat_{sent_to_user}'
        await self.channel_layer.group_send(
            self.other_user_chat_room,
            {
                'type': 'receive_group_message',
                'message': message,
                'username': username,
                'sent_by_user': sent_by_user,
                'sent_to_user': sent_to_user,
            }
        )
    
    async def receive_group_message(self, event):
        message = event['message']
        username = event['username']
        sent_by_user = event['sent_by_user']
        sent_to_user = event['sent_to_user']

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps({
            'message': message,
            'username': username,
            'sent_by_user': sent_by_user,
            'sent_to_user': sent_to_user,
        }))
    
    @database_sync_to_async
    def get_user_object(self, user_id):
        qs = User.objects.filter(id=user_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return str(obj.id)