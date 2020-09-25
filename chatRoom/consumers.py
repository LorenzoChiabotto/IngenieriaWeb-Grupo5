# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        aType = text_data_json['type']
        message = text_data_json['message']
        userId = text_data_json['userId']
        userName = text_data_json['userName']
        image = text_data_json['image']
        aFile = text_data_json['file']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':aType,
                'message': message,
                'userId':userId,
                'userName':userName,
                'image':image,
                'file':aFile,
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        aType = event['type']
        message = event['message']
        userId = event['userId']
        userName = event['userName']
        image = event['image']
        aFile = event['file']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type':aType,
            'message': message,
            'userId':userId,
            'userName':userName,
            'image':image,
            'file':aFile,
        }))