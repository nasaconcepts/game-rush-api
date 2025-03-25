"""
ASGI config for gamerushapi project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# configure graphql
from channels.routing import ProtocolTypeRouter, URLRouter
from ariadne.asgi import GraphQL
from channels_graphql_ws import GraphQLSubscriptionConsumer
from django.urls import path
from .schema import schema


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamerushapi.settings')

# application = get_asgi_application() <- original application setup


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
        path("graphql/", GraphQLSubscriptionConsumer.as_asgi(schema=schema)),
    ]),
})
