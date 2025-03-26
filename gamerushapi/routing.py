from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
# from graphene_subscriptions.consumers import GraphqlSubscriptionConsumer
from channels_graphql_ws import GraphqlWsConsumer
from channels.auth import get_user

class MyGraphqlWsConsumer(GraphqlWsConsumer):
    schema = "api.graphql.schema.schema"

    async def on_connect(self, payload):
        self.scope["user"] = await get_user(self.scope)

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("graphql/", MyGraphqlWsConsumer.as_asgi()),
        ])
    ),
})