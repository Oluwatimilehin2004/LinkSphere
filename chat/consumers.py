# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_anonymous:
            await self.close()
        else:
            self.user_group_name = f'user_{self.user.username}'
            await self.channel_layer.group_add(
                self.user_group_name,
                self.channel_name
            )
            await self.accept()
            print(f"User {self.user.username} connected.")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.user_group_name,
            self.channel_name
        )
        print(f"User {self.user.username} disconnected.")

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        recipient_username = text_data_json.get('recipient')

        print(f"Received message from {self.user.username} to {recipient_username}: {message}")

        if recipient_username:
            await self.channel_layer.group_send(
                f'user_{recipient_username}',
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': self.user.username
                }
            )

    async def chat_message(self, event):
        message = event['message']
        sender = event.get('sender', 'System')
        print(f"Sending message to {self.user.username} from {sender}: {message}")
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))