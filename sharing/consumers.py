from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.utils import timezone
from datetime import datetime
from sharing.models import Flats, SystemLogs
from channels.db import database_sync_to_async
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        #self.auth_key = self.scope['url_route']['kwargs']['auth_key']
        self.room_group_name = 'chat_%s' % self.room_name
        

        print("=== Connected {0} {1}".format(self.room_group_name,datetime.now()))
        await self.addLog(self.room_name,comment="Connected")
        if await self.get_flat(self.room_name) is True:
            await self.channel_layer.group_add('events', self.channel_name)
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.update_flat_status(self.room_name,True)
            await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        print("Disconnect {0} {1}".format(self.room_group_name,datetime.now()))
        await self.update_flat_status(self.room_name,False)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.addLog(self.room_name,comment="Disconnected")

    @database_sync_to_async
    def get_flat(self,id):
        return Flats.flas.get_flat(id)

    @database_sync_to_async
    def update_flat_status(self,id,status):
        Flats.flas.update_flat_status(id,status)
        return True

    @database_sync_to_async
    def addLog(self,id,comment):
        SystemLogs.objects.create(device_id=int(id),created_at=timezone.now(),comment=comment)
        return True

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = text_data
        message = text_data#text_data_json['message']
        print("Received new message form {0}, {1}".format(self.room_group_name,message))
        await self.addLog(self.room_name,comment=message)
        # Send message to room group
        '''
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        '''

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
    

    async def channel_message(self, event):
        message = event['message']
        appid = event['appid']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'appid':appid,
            #'TEMP_KEY': self.auth_key
        }))

