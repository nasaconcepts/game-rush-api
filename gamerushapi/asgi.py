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
from api.graphql.ariadne.routing import websocket_urlpatterns
# from graphql_ws.django_channels import GraphQLWsConsumer
from django.urls import path, re_path
# from ariadne.asgi import GraphQL



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamerushapi.settings')

# django_application = get_asgi_application() 

# async def application(scope, receive, send):
#     if scope['type'] == 'http':
#         await django_application(scope, receive, send)
#     else:
#         await websocket_application(scope, receive, send)

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),  # Handles normal HTTP requests
#     "websocket": GraphQL(schema),    # Handles GraphQL subscriptions
# })

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": URLRouter(websocket_urlpatterns),
# })
graphql_app = GraphQL(schema, debug=True)
# application = ProtocolTypeRouter(
#     {
#         "http": get_asgi_application(),
#         "websocket": URLRouter([
#             path("graphql", GraphQLWsConsumer.as_asgi()),
#         ]),
#     }
# )


application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Django's ASGI application for HTTP
    "websocket": URLRouter([
        path("api/graphql", graphql_app),  # WebSocket path for GraphQL subscriptions
    ]),
})