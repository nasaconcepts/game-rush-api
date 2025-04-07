from channels.generic.websocket import AsyncWebsocketConsumer
import json
from api.graphql.ariadne.schema import schema
from ariadne import graphql

class GraphqlSubscriptionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        print(f"I was accepted...")
        await self.accept()

    async def disconnect(self, close_code):
        # Handle WebSocket disconnection
        print(f"I am disconnecting...")
        pass

    # async def receive(self, text_data):
    #     print(f"i have received {text_data}")
    #     data = json.loads(text_data)
    #     if data.get("type") == "connection_init":
    #         await self.send(text_data=json.dumps({"type": "connection_ack"}))
    #     elif data.get("type") == "start":
    #         result = await graphql_app.graphql(data)
    #         if hasattr(result, "__aiter__"): #If the result is Async Generator.
    #             async for item in result:
    #                 await self.send(text_data=json.dumps(item))
    #         else:
    #             await self.send(text_data=json.dumps(result))
    #     elif data.get("type") == "stop":
    #         pass # Stop subscription.
    async def receive(self, text_data):
        print(f"i have received {text_data}")
        data = json.loads(text_data)
        operation_type = data.get("type")
        payload = data.get("payload")

        if operation_type == "connection_init":
            await self.send(text_data=json.dumps({"type": "connection_ack"}))

        elif operation_type == "start":
            query = payload.get("query")
            variables = payload.get("variables")
            operation_name = payload.get("operationName")

            success, result = await graphql(
                schema,
                {"query": query, "variables": variables, "operationName": operation_name},
                context_value={"request": self.scope}, # Passes the scope to the resolvers.
            )

            if success:
                if hasattr(result, "__aiter__"):
                    async for item in result:
                        await self.send(text_data=json.dumps({"type": "next", "payload": item}))
                else:
                    await self.send(text_data=json.dumps({"type": "next", "payload": result}))

            else:
                await self.send(text_data=json.dumps({"type": "errors", "payload": result}))

        elif operation_type == "stop":
            pass # Handle stop operation.

        elif operation_type == "connection_terminate":
            await self.close()