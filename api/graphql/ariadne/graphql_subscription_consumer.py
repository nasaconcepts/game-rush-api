from channels.generic.websocket import AsyncWebsocketConsumer
import json

class GraphqlSubscriptionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        print(f"I was accepted...")
        await self.accept()

    async def disconnect(self, close_code):
        # Handle WebSocket disconnection
        print(f"I am disconnecting...")
        pass

    async def receive(self, text_data):
        # Handle messages received from the WebSocket
        print(f"I was received...")
        data = json.loads(text_data)
        # Process the received data
        await self.send(text_data=json.dumps({
            'message': 'Message received',
            'data': data
        }))