from email import message
# import imp
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Message, Room
from accounts.models import User
from accounts.serializers import MinimalUserSerializer
from .generator import Generator
import logging

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' %self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print(f"Added {self.channel_name} channel to {self.room_group_name} group")
        await self.accept()
    
    async def disconnect(self, code=None):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"Removed {self.channel_name} channel from {self.room_group_name} group")
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['data']['content']
        user = data['data']['user']
        room = data['data']['room']
        read_by = data['data']['read_by']
        isPrompted = data['data']['isPrompted']

        print(f"Received message: {message} from {user} in room {room} and read by {read_by}")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user,
                'room': room,
                'read_by': read_by
            }
        )
        
        if isPrompted:
            print(f"Prompting GPT-3 for response in room {room}")
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'gpt_message',
                    'message': message,
                    'user': user,
                    'room': room,
                    'read_by': read_by
                }
            )

    
    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        room = event['room']
        read_by = event['read_by']

        await self.save_message(user, room, message)

        print(f"Sent message: {message} from {user} in room {room}")
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'room': room,
            'read_by': read_by
        }))

    async def gpt_message(self, event):
        try:
            user = event['user']
            message = event['message']
            room = event['room']
            read_by = event['read_by']
            algofriend = await sync_to_async(User.objects.filter(email='algofriend@algoway.com').first)()
            if algofriend is not None:
                algofriend_data = MinimalUserSerializer(algofriend).data
            else:
                algofriend_data = None
            
            read_by.append(algofriend_data['id'])

            GPT = Generator(user)
            message = await GPT.generated_answer(message)
            
            await self.save_message(algofriend_data, room, message) 
            await self.send(text_data=json.dumps({
                'message': message,
                'user': algofriend_data,
                'room': room,
                'read_by': read_by
            }))

        except Exception as e:
            print("Something while generating went wrong here ...")
            return None
        

    @sync_to_async
    def save_message(self, user, room, message):
        user = User.objects.get(id=user['id'])
        room = Room.objects.get(id=room)
        Message.objects.create(user=user, room=room, content=message)
        print(f"Saved message: {message} from {user} in room {room}")