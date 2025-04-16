import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone


class ChatbotConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.room_group_name = f"chatbot_{self.session_id}"

        # Join room group if channel layer exists
        if self.channel_layer is not None:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
        await self.accept()

        # Send welcome message
        await self.send(text_data=json.dumps({
            "message": "Hello! How can I help you with your floral needs today?",
            "sender": "bot",
        }))

    async def disconnect(self, close_code):
        # Leave room group if channel layer exists
        if self.channel_layer is not None:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        # Parse incoming data
        data = json.loads(text_data)
        message = data.get('message', '')

        # Get bot response
        bot_response = self.get_bot_response(message)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': bot_response,
            'sender': 'bot'
        }))

    def get_bot_response(self, message):
        # No changes in this method
        if not message:
            return "I didn't catch that. Could you please repeat?"

        message = message.lower()

        if "roses" in message:
            return "Yes, we have various colors of roses available. Would you like to see our collection?"
        elif "delivery" in message:
            return "We offer same-day delivery for orders placed before 2 PM, and next-day delivery for later orders."
        elif "custom" in message:
            return "You can create a custom bouquet by visiting our Custom Bouquets section or specifying your preferences here!"
        elif "track" in message:
            return "Please provide your order number, and I'll check its status for you."
        else:
            return "Thank you for your message. How else can I assist you with your floral needs today?"
