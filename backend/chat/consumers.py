import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import sync_to_async
from .models import Room


class ChatConsumer(AsyncWebsocketConsumer):
    # async def connect(self):
    #     user = self.scope["user"]
    #     if user.is_authenticated:
    #         await self.accept()
    #     else:
    #         await self.close()
    #     self.room_name = "chat"
    #     self.room_group_name = f"chat_{self.room_name}"
    #
    #     # Join room group
    #     await self.channel_layer.group_add(
    #         self.room_group_name,
    #         self.channel_name
    #     )
    #     await self.accept()
    async def connect(self):
        user = self.scope['user']
        room_name = self.scope['url_route']['kwargs']['room_name']

        if user.is_authenticated:
            # Check if the user is allowed in the room
            is_member = await sync_to_async(Room.objects.filter(name=room_name, members=user).exists)()
            if is_member:
                await self.accept()
            else:
                await self.close()
        else:
            await self.close()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
            }
        )

    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
