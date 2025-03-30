"""
ASGI config for gamerushapi project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
# from ariadne.asgi import GraphQLTransportWSHandler

# configure graphql


# from django.urls import path
# from api.graphql.ariadne.routing import application as websocket_application
from channels.routing import ProtocolTypeRouter,URLRouter
from ariadne.asgi import GraphQL
from api.graphql.ariadne.schema import schema
from api.graphql.ariadne.graphql_subscription_consumer import GraphqlSubscriptionConsumer
# from graphql_ws.django_channels import GraphQLWsConsumer
from django.urls import path, re_path
# from ariadne.asgi import GraphQL



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamerushapi.settings')


graphql_app = GraphQL(schema, debug=True)
websocket_urlpatterns = [
    path("api/graphql", GraphqlSubscriptionConsumer.as_asgi()),
]


application = ProtocolTypeRouter({
    "http": graphql_app,  # Django's ASGI application for HTTP
    "websocket": URLRouter(websocket_urlpatterns),  # WebSocket path for GraphQL subscriptions
})