"""
WSGI config for gamerushapi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from channels.routing import ProtocolTypeRouter
from ariadne.asgi import GraphQL
from api.graphql.ariadne.schema import schema
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamerushapi.settings')

application = get_wsgi_application()
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),  # Handles normal HTTP requests
#     "websocket": GraphQL(schema),    # Handles GraphQL subscriptions
# })
